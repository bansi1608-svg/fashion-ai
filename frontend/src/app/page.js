"use client";

import { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function Home() {
  // --- All products (loaded once on page load) ---
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Search ---
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [parsedQuery, setParsedQuery] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/products`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch products");
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
  }, []);

  function handleSearchSubmit(e) {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearchLoading(true);
    setSearchError(null);

    fetch(`${API_BASE_URL}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: searchQuery }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Search failed");
        return response.json();
      })
      .then((data) => {
        setSearchResults(data.results);
        setParsedQuery(data.parsed_query);
        setSearchLoading(false);
      })
      .catch((err) => {
        setSearchError(err.message);
        setSearchLoading(false);
      });
  }

  function clearSearch() {
    setSearchQuery("");
    setSearchResults(null);
    setParsedQuery(null);
  }

  if (loading) return <main className="p-8">Loading products...</main>;
  if (error) {
    return (
      <main className="p-8 text-red-600">
        Error loading products: {error}
        <br />
        (Is the backend running at {API_BASE_URL} ?)
      </main>
    );
  }

  const displayedProducts = searchResults !== null ? searchResults : products;
  const sectionTitle =
    searchResults !== null
      ? `Search Results (${searchResults.length})`
      : "All Products";

  return (
    <main className="p-8 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Fashion Discovery</h1>
      <p className="text-gray-500 mb-6">
        Describe what you want, in your own words.
      </p>

      <form onSubmit={handleSearchSubmit} className="mb-4 flex gap-3">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="e.g. baddie outfit under ₹2500"
          className="flex-1 border rounded px-4 py-3 text-lg"
        />
        <button
          type="submit"
          className="bg-black text-white px-6 py-3 rounded"
        >
          Search
        </button>
        {searchResults !== null && (
          <button
            type="button"
            onClick={clearSearch}
            className="text-sm underline whitespace-nowrap"
          >
            Clear
          </button>
        )}
      </form>

      {searchLoading && <p className="mb-4">Searching...</p>}
      {searchError && <p className="mb-4 text-red-600">{searchError}</p>}

      {parsedQuery && (
        <div className="mb-8 text-sm bg-gray-100 rounded px-4 py-3">
          <span className="font-semibold">Understood:</span>{" "}
          style: {parsedQuery.style ?? "not detected"} · colour:{" "}
          {parsedQuery.colour ?? "not detected"} · category:{" "}
          {parsedQuery.category ?? "not detected"} · budget:{" "}
          {parsedQuery.budget !== null ? `₹${parsedQuery.budget}` : "no limit specified"}
        </div>
      )}

      <h2 className="text-xl font-semibold mb-4">{sectionTitle}</h2>

      {displayedProducts.length === 0 ? (
        <p className="text-gray-500">
          No products matched your search. Try different words.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {displayedProducts.map((product) => (
            <div key={product.id} className="border rounded-lg p-4 shadow-sm">
              {"match_score" in product && (
                <span className="inline-block bg-black text-white text-xs px-2 py-1 rounded mb-2">
                  {product.match_score}% match
                </span>
              )}
              <h3 className="font-semibold text-lg">{product.name}</h3>
              <p className="text-gray-600">{product.brand}</p>
              <p className="mt-2 font-bold">₹{product.price}</p>
              <p className="text-sm text-gray-500">
                {product.colour} · {product.category}
              </p>
              <a
                href={product.product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-3 text-sm underline"
              >
                Shop Now →
              </a>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}