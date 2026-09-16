"use client";

import { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function Home() {
  // --- All products (loaded once on page load) ---
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Search form state ---
  const [formValues, setFormValues] = useState({
    style: "",
    colour: "",
    category: "",
    budget: "",
  });

  // --- Search results (null = no search performed yet) ---
  const [searchResults, setSearchResults] = useState(null);
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

  function handleChange(e) {
    setFormValues((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSearchLoading(true);
    setSearchError(null);

    fetch(`${API_BASE_URL}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        style: formValues.style,
        colour: formValues.colour,
        category: formValues.category,
        budget: Number(formValues.budget),
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Search failed");
        return response.json();
      })
      .then((data) => {
        setSearchResults(data);
        setSearchLoading(false);
      })
      .catch((err) => {
        setSearchError(err.message);
        setSearchLoading(false);
      });
  }

  function clearSearch() {
    setSearchResults(null);
    setFormValues({
      style: "",
      colour: "",
      category: "",
      budget: "",
    });
  }

  if (loading) {
    return <main className="p-8">Loading products...</main>;
  }

  if (error) {
    return (
      <main className="p-8 text-red-600">
        Error loading products: {error}
        <br />
        (Is the backend running at {API_BASE_URL}?)
      </main>
    );
  }

  const displayedProducts =
    searchResults !== null ? searchResults : products;

  const sectionTitle =
    searchResults !== null
      ? `Search Results (${searchResults.length})`
      : "All Products";

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">
        Fashion Discovery
      </h1>

      <form
        onSubmit={handleSubmit}
        className="mb-8 flex flex-wrap gap-4 items-end border-b pb-6"
      >
        <div>
          <label className="block text-sm mb-1">
            Style
          </label>

          <input
            name="style"
            value={formValues.style}
            onChange={handleChange}
            placeholder="e.g. baddie"
            className="border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">
            Colour
          </label>

          <input
            name="colour"
            value={formValues.colour}
            onChange={handleChange}
            placeholder="e.g. black"
            className="border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">
            Category
          </label>

          <input
            name="category"
            value={formValues.category}
            onChange={handleChange}
            placeholder="e.g. top"
            className="border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">
            Budget (₹)
          </label>

          <input
            name="budget"
            type="number"
            value={formValues.budget}
            onChange={handleChange}
            placeholder="e.g. 1000"
            className="border rounded px-3 py-2 w-28"
          />
        </div>

        <button
          type="submit"
          className="bg-black text-white px-4 py-2 rounded"
        >
          Search
        </button>

        {searchResults !== null && (
          <button
            type="button"
            onClick={clearSearch}
            className="text-sm underline"
          >
            Clear search
          </button>
        )}
      </form>

      {searchLoading && <p>Searching...</p>}

      {searchError && (
        <p className="text-red-600">{searchError}</p>
      )}

      <h2 className="text-xl font-semibold mb-4">
        {sectionTitle}
      </h2>

      {displayedProducts.length === 0 ? (
        <p className="text-gray-500">
          No products matched your search. Try adjusting your criteria.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {displayedProducts.map((product) => (
            <div
              key={product.id}
              className="border rounded-lg p-4 shadow-sm"
            >
              {"match_score" in product && (
                <span className="inline-block bg-black text-white text-xs px-2 py-1 rounded mb-2">
                  {product.match_score}% match
                </span>
              )}

              <h3 className="font-semibold text-lg">
                {product.name}
              </h3>

              <p className="text-gray-600">
                {product.brand}
              </p>

              <p className="mt-2 font-bold">
                ₹{product.price}
              </p>

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
