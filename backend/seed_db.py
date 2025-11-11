from database import SessionLocal, create_tables, Post, ChatMessage

def seed_database():
    """Seed the database with initial data"""
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Post).count() > 0:
            print("Database already contains posts. Skipping seeding.")
            return
        
        # Sample blog posts
        posts_data = [
            {
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
        
        # Create blog posts
        for post_data in posts_data:
            post = Post(**post_data)
            db.add(post)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()