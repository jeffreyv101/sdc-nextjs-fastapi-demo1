// Dummy imports
import { getPosts } from '@/lib/posts'
import { Post } from '@/components/post'
import Header from '@/components/header.js'
 
export default async function Page() {
  const posts = await getPosts()
 
  return (
    <div>
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-8">
            {posts.length > 0 ? (
                <ul className="space-y-0">
                {posts.map((post) => (
                    <Post key={post.id} post={post} />
                ))}
                </ul>
            ) : (
                <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No blog posts found.</p>
                </div>
            )}
        </div>
    </div>
  )
}