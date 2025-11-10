from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables, Post, ChatMessage
from seed_db import seed_database

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
def post_ai_chat_message(message: dict, db: Session = Depends(get_db)):
    """Receive a message from the user and return a sample AI response"""
    user_message = message.get("content", "")
    
    # Save user message to database
    user_msg = ChatMessage(role="user", content=user_message)
    db.add(user_msg)
    
    # In a real application, you would process the user message and generate a response
    ai_response_content = f"You said: {user_message}. This is a sample response from the AI."
    
    # Save AI response to database
    ai_msg = ChatMessage(role="assistant", content=ai_response_content)
    db.add(ai_msg)
    
    db.commit()
    
    return {"role": "assistant", "content": ai_response_content}