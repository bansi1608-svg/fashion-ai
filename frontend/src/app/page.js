"use client";

import { useState, useEffect } from "react";
import ProductCard from "./components/ProductCard";
import { logInteraction } from "./lib/interactions";


const API_BASE_URL = "http://127.0.0.1:8000";

export default function Home() {
  // --- All products ---
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Text search ---
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [parsedQuery, setParsedQuery] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState(null);

  // --- Visual search ---
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [visualResults, setVisualResults] = useState(null);
  const [visualLoading, setVisualLoading] = useState(false);
  const [visualError, setVisualError] = useState(null);

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

  function handleShopClick(productId) {
  logInteraction({ interactionType: "click", productId });
}

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
        logInteraction({
          interactionType: "search",
          style: data.parsed_query.style,
          colour: data.parsed_query.colour,
          category: data.parsed_query.category,
        });
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

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setVisualResults(null);
    setVisualError(null);
  }

  function handleVisualSearchSubmit(e) {
    e.preventDefault();
    if (!selectedFile) return;

    setVisualLoading(true);
    setVisualError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    // NOTE: no "Content-Type" header set here on purpose - the browser
    // sets the correct multipart boundary automatically for FormData.
    // Setting it manually would break the upload.
    fetch(`${API_BASE_URL}/visual-search?limit=6`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Visual search failed");
        return response.json();
      })
      .then((data) => {
        setVisualResults(data);
        setVisualLoading(false);
        logInteraction({ interactionType: "visual_search" });
      })
      .catch((err) => {
        setVisualError(err.message);
        setVisualLoading(false);
      });
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
        Describe what you want, or upload a photo to find similar items.
      </p>

      {/* --- Text search --- */}
      <form onSubmit={handleSearchSubmit} className="mb-4 flex gap-3">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="e.g. baddie outfit under ₹2500"
          className="flex-1 border rounded px-4 py-3 text-lg"
        />
        <button type="submit" className="bg-black text-white px-6 py-3 rounded">
          Search
        </button>
        {searchResults !== null && (
          <button type="button" onClick={clearSearch} className="text-sm underline whitespace-nowrap">
            Clear
          </button>
        )}
      </form>

      {searchLoading && <p className="mb-4">Searching...</p>}
      {searchError && <p className="mb-4 text-red-600">{searchError}</p>}

      {parsedQuery && (
        <div className="mb-8 text-sm bg-gray-100 rounded px-4 py-3">
          <span className="font-semibold">Understood:</span> style:{" "}
          {parsedQuery.style ?? "not detected"} · colour:{" "}
          {parsedQuery.colour ?? "not detected"} · category:{" "}
          {parsedQuery.category ?? "not detected"} · budget:{" "}
          {parsedQuery.budget !== null ? `₹${parsedQuery.budget}` : "no limit specified"}
        </div>
      )}

      {/* --- Visual search --- */}
      <div className="mb-8 border-t pt-6">
        <h2 className="text-lg font-semibold mb-3">Find clothes like this</h2>
        <form onSubmit={handleVisualSearchSubmit} className="flex items-center gap-4">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button
            type="submit"
            disabled={!selectedFile}
            className="bg-indigo-600 text-white px-4 py-2 rounded disabled:opacity-40"
          >
            Find Similar
          </button>
        </form>

        {previewUrl && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={previewUrl} alt="Preview" className="mt-4 h-40 rounded border" />
        )}

        {visualLoading && <p className="mt-3">Searching visually...</p>}
        {visualError && <p className="mt-3 text-red-600">{visualError}</p>}

        {visualResults !== null && (
          <div className="mt-6">
            <h3 className="font-semibold mb-3">
              Visually Similar Products ({visualResults.length})
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {visualResults.map((product) => (
                <ProductCard key={product.id} product={product} onShopClick={handleShopClick} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* --- Main product grid --- */}
      <h2 className="text-xl font-semibold mb-4">{sectionTitle}</h2>

      {displayedProducts.length === 0 ? (
        <p className="text-gray-500">No products matched your search. Try different words.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {displayedProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </main>
  );
}