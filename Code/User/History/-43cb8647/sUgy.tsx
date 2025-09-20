import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Welcome to the Shop</h1>
      <div className="space-x-4">
        <Link href="/products" className="btn">
          Products
        </Link>
        <Link href="/cart" className="btn">
          Cart
        </Link>
        <Link href="/admin" className="btn">
          Admin
        </Link>
      </div>
    </div>
  );
}
