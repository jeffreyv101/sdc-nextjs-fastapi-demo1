from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables, Post, ChatMessage
from seed_db import seed_database
from ollama_service import ollama_service

app = FastAPI()

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    seed_database()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/posts")
def get_posts(db: Session = Depends(get_db)):
    """Get all blog posts from database"""
    posts = db.query(Post).all()
    return {"posts": [
        {
            "id": post.id,
            "slug": post.slug,
            "title": post.title,
            "excerpt": post.excerpt,
            "content": post.content,
            "author": post.author
        } for post in posts
    ]}


@app.get("/api/posts/{slug}")
def get_post(slug: str, db: Session = Depends(get_db)):
    """Get a single blog post by slug from database"""
    post = db.query(Post).filter(Post.slug == slug).first()
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "id": post.id,
        "slug": post.slug,
        "title": post.title,
        "excerpt": post.excerpt,
        "content": post.content,
        "author": post.author
    }

@app.get("/api/ai-chat/messages")
def get_ai_chat_messages(db: Session = Depends(get_db)):
    """Get AI chat messages from database"""
    messages = db.query(ChatMessage).order_by(ChatMessage.created_at).all()
    return {"messages": [
        {
            "role": message.role,
            "content": message.content
        } for message in messages
    ]}

@app.post("/api/ai-chat/message")
async def post_ai_chat_message(message: dict, db: Session = Depends(get_db)):
    """Receive a message from the user and return an AI response from Ollama"""

    messages = db.query(ChatMessage).order_by(ChatMessage.created_at).all()

    # Build a text history from past messages and append the current user content
    history = " ".join([f"{m.role}: {m.content}" for m in messages])
    user_message = "You are a sassy teenager. " + (history + " " if history else "") + message.get("content", "")
    
    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    
    # Save user message to database
    user_msg = ChatMessage(role="user", content=user_message)
    db.add(user_msg)
    db.flush()  # Flush to get the ID but don't commit yet
    
    try:
        # Generate AI response using Ollama
        ai_response_content = await ollama_service.generate_response(user_message)
        
        # If Ollama is not available, fall back to a default response
        if ai_response_content is None:
            ai_response_content = "Sorry, I'm currently unavailable. Please make sure Ollama is running and try again."
        
        # Save AI response to database
        ai_msg = ChatMessage(role="assistant", content=ai_response_content)
        db.add(ai_msg)
        
        # Commit both messages
        db.commit()
        
        return {"role": "assistant", "content": ai_response_content}
        
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        print(f"Error generating AI response: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI response")

@app.get("/api/ollama/models")
async def get_ollama_models():
    """Get list of available Ollama models"""
    try:
        models = await ollama_service.list_models()
        return {"models": models}
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch available models")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on app shutdown"""
    await ollama_service.close()