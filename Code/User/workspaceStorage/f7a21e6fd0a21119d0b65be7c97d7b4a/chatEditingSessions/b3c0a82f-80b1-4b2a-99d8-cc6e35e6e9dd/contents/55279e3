import { products } from "@/lib/products";
import Link from "next/link";
import { useCart } from "@/components/CartContext";

export default function ProductsPage() {
  // useCart only works in client components, so this is a server component for listing
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Products</h2>
      <ul className="space-y-4">
        {products.map((p) => (
          <li key={p.id} className="border p-4 rounded">
            <div className="font-semibold">{p.name}</div>
            <div>{p.description}</div>
            <div className="font-bold">${p.price}</div>
            <Link href={`/products/${p.id}`} className="btn mt-2 inline-block">
              View
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
