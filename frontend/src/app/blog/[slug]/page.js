import { getPost } from '@/lib/posts';
import Link from 'next/link';

export default async function BlogPostPage({ params }) {
  const { slug } = await params
  const post = await getPost(slug)
 
  return (
    <article className="max-w-4xl mx-auto px-4 py-8">
      <header className="mb-8">
        <Link 
          href="/blog"
          className="inline-flex items-center text-blue-700 dark:text-blue-400 hover:text-blue-600 mb-6 transition-colors duration-200"
        >
          <svg 
            className="mr-2 w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M15 19l-7-7 7-7" 
            />
          </svg>
          Back to Blog
        </Link>
        
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-300 mb-4 leading-tight">
          {post.title}
        </h1>
        
        <div className="flex items-center text-gray-500 dark:text-gray-400 mb-4">
          <span>By {post.author}</span>
        </div>
      </header>
      
      <div className="prose prose-lg max-w-none">
        {post.content.split('\n').map((paragraph, index) => (
          paragraph.trim() && (
            <p key={index} className="mb-4 text-gray-900 dark:text-gray-100 leading-relaxed">
              {paragraph.trim()}
            </p>
          )
        ))}
      </div>
    </article>
  )
}