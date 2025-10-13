import Header from '@/components/header.js';

export default function Home() {
  return (
    <>
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-4">Welcome to My Next.js App</h2>
        <p className="text-md text-gray-400">
          This is the home page. Use the navigation links above to explore the blog and other pages.
        </p>
      </main>
    </>
  );
}
