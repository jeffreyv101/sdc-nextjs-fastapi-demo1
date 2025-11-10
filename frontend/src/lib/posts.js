// Configuration for the FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Get all posts
export async function getPosts() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/posts`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.posts;

  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
}

// Get a single post by slug
export async function getPost(slug) {
  try {
    // Fetch a single post from the backend
    const response = await fetch(`${API_BASE_URL}/api/posts/${slug}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Post not found');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const post = await response.json();

    return post;
  } catch (error) {
    console.error('Error fetching post:', error);
    throw error;
  }
}