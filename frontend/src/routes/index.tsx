import { createFileRoute } from '@tanstack/react-router';
import { useEffect, useState } from 'react';

export const Route = createFileRoute('/')({
  component: Index,
});

interface TrendingBook {
  product_id: number;
  title: string;
  authors: string;
  avg_rating: number;
  n_review: number;
  cover_link: string;
  trending_score: number;
}

function Index() {
  const [books, setBooks] = useState<TrendingBook[]>([]);

  useEffect(() => {
    fetch('/api/trending-books')
      .then((res) => res.json())
      .then((data) => setBooks(data))
      .catch((err) => console.error('Error fetching books:', err));
  }, []);

  return (
    <div className="p-6">
      <h3 className="text-2xl font-bold mb-4">Trending Books</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {books.map((book) => (
          <BookCard key={book.product_id} book={book} />
        ))}
      </div>
    </div>
  );
}

function BookCard({ book }: { book: TrendingBook }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4 hover:shadow-xl transition">
      <img
        src={book.cover_link}
        alt={book.title}
        className="w-full h-48 object-cover rounded-md"
      />
      <h4 className="mt-3 text-lg font-semibold">{book.title}</h4>
      <p className="text-gray-600 text-sm">by {book.authors}</p>
      <p className="mt-2 text-yellow-500 font-bold">⭐ {book.avg_rating}</p>
    </div>
  );
}
