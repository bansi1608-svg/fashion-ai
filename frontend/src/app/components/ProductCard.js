// frontend/src/app/components/ProductCard.js
//
// One product card, reused wherever we display product results -
// the full catalogue grid, text search results, and visual search
// results all use this same component now.

export default function ProductCard({ product }) {
  return (
    <div className="border rounded-lg p-4 shadow-sm">
      {"match_score" in product && (
        <span className="inline-block bg-black text-white text-xs px-2 py-1 rounded mb-2">
          {product.match_score}% match
        </span>
      )}
      {"similarity_score" in product && (
        <span className="inline-block bg-indigo-600 text-white text-xs px-2 py-1 rounded mb-2">
          {product.similarity_score}% similar
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
  );
}