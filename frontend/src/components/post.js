import Link from 'next/link';

export function Post({ post }) {
  return (
    <li className="mb-8 p-6 bg-gray-200 dark:bg-gray-700 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
      <article>
        <header className="mb-4">
          <h2 className="text-2xl font-bold dark:text-gray-100 mb-2">
            <Link 
              href={`/blog/${post.slug}`} 
              className="hover:text-blue-600 transition-colors duration-200"
            >
              {post.title}
            </Link>
          </h2>
          <div className="flex items-center text-sm dark:text-gray-400 mb-2">
            <span>By {post.author}</span>
          </div>
        </header>
        <p className="text-gray-900 dark:text-gray-300 mb-4 leading-relaxed">
          {post.excerpt}
        </p>
        <Link 
          href={`/blog/${post.slug}`}
          className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
        >
          Read more
        </Link>
      </article>
    </li>
  );
}