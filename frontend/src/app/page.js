"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/products")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        return response.json();
      })
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []); // empty array = run once, when the page first loads

  if (loading) {
    return <main className="p-8">Loading products...</main>;
  }

  if (error) {
    return (
      <main className="p-8 text-red-600">
        Error loading products: {error}
        <br />
        (Is the backend running at http://127.0.0.1:8000 ?)
      </main>
    );
  }

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">Fashion Discovery</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.id} className="border rounded-lg p-4 shadow-sm">
            <h2 className="font-semibold text-lg">{product.name}</h2>
            <p className="text-gray-600">{product.brand}</p>
            <p className="mt-2 font-bold">₹{product.price}</p>
            <p className="text-sm text-gray-500">
              {product.colour} · {product.category}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}