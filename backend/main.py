from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample blog posts data
posts = [
    {
        "id": 1,
        "slug": "getting-started-with-nextjs",
        "title": "Getting Started with Next.js",
        "excerpt": "Learn the basics of Next.js and how to build modern web applications.",
        "content": """
      Next.js is a powerful React framework that makes it easy to build modern web applications.
      
      With features like server-side rendering, static site generation, and API routes,
      Next.js provides everything you need to build production-ready applications.
      
      In this post, we'll explore the key concepts and get you started with your first Next.js project.
    """,
        "author": "John Doe",
    },
    {
        "id": 2,
        "slug": "mastering-tailwind-css",
        "title": "Mastering Tailwind CSS",
        "excerpt": "Discover how to use Tailwind CSS to build beautiful, responsive designs quickly.",
        "content": """
      Tailwind CSS is a utility-first CSS framework that allows you to build custom designs
      without writing custom CSS.
      
      By using utility classes, you can create responsive layouts, handle hover states,
      and build complex components all within your HTML.
      
      This post will show you advanced techniques for getting the most out of Tailwind CSS.
    """,
        "author": "Jane Smith"
    },
    {
        "id": 3,
        "slug": "react-best-practices",
        "title": "React Best Practices for 2024",
        "excerpt": "Learn the latest React patterns and best practices to write better code.",
        "content": """
      React continues to evolve, and with it, the best practices for building
      maintainable and performant applications.
      
      In this comprehensive guide, we'll cover component composition, state management,
      performance optimization, and testing strategies.
      
      Whether you're a beginner or experienced developer, these practices will
      help you write better React code.
    """,
        "author": "Mike Johnson"
    }
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/posts")
def get_posts():
    """Get all blog posts"""
    return {"posts": posts}


@app.get("/api/posts/{slug}")
def get_post(slug: str):
    """Get a single blog post by slug"""
    post = None

    for p in posts:
        if p["slug"] == slug:
            post = p
            break
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

