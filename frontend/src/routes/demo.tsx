import { createFileRoute } from '@tanstack/react-router';
import { useState } from 'react';
import axios from 'axios';

export const Route = createFileRoute('/demo')({
  component: RouteComponent,
});

interface Book {
  product_id: number;
  title: string;
  authors: string;
  avg_rating: number;
  n_review: number;
  cover_link: string;
}

function RouteComponent() {
  const [userId, setUserId] = useState('');
  const [productId, setProductId] = useState('');
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!userId && !productId) {
        setError('Please provide at least a User ID or Book ID.');
        return;
      }

      const endpoint =
        userId && productId
          ? `api/hybrid-recommendations?user_id=${userId}&product_id=${productId}`
          : userId
            ? `api/cf-recommendations?user_id=${userId}`
            : `api/cbf-recommendations?product_id=${productId}`;

      try {
        const response = await axios.get<Book[]>(endpoint);
        setBooks(response.data);
      } catch {
        setError('Failed to fetch recommendations.');
      }
    } catch (err) {
      setError('Failed to fetch recommendations.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Book Recommendations</h2>

      <div className="mb-4 space-y-2">
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter User ID"
          className="border p-2 w-full rounded-md"
        />
        <input
          type="text"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          placeholder="Enter Book ID"
          className="border p-2 w-full rounded-md"
        />
        <button
          onClick={fetchRecommendations}
          className="bg-blue-500 text-white px-4 py-2 rounded-md w-full hover:bg-blue-600 cursor-pointer"
        >
          Get Recommendations
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <h3 className="text-lg font-semibold mt-6">Recommended Books</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {books.map((book) => (
          <div
            key={book.product_id}
            className="border p-4 rounded-md shadow-md"
          >
            <img
              src={book.cover_link}
              alt={book.title}
              className="w-full h-48 object-cover rounded-md"
            />
            <h3 className="text-lg font-semibold mt-2">{book.title}</h3>
            <p className="text-sm text-gray-600">by {book.authors}</p>
            <p className="text-sm">
              ⭐ {book.avg_rating} ({book.n_review} reviews)
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
