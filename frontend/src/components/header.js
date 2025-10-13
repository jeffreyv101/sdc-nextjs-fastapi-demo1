import Link from 'next/link';

export default function Header() {
    return (
        <header className="bg-gray-800 text-white p-4 mb-8">
            <div className="max-w-4xl mx-auto flex justify-between items-center">
                <h1 className="text-2xl font-bold">My Next.js App</h1>
                <nav>
                    <Link href="/" className="text-gray-300 hover:text-white mx-2">Home</Link>
                    <Link href="/blog" className="text-gray-300 hover:text-white mx-2">Blog</Link>
                    <Link href="/hello-world" className="text-gray-300 hover:text-white mx-2">Hello World</Link>
                </nav>
            </div>
        </header>
    );
}