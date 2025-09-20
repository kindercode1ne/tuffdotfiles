"use client";
import { products } from '@/lib/products';
import Link from 'next/link';
import { useCart } from '@/components/CartContext';

export default function ProductDetail({ params }: { params: { id: string } }) {
  const product = products.find((p) => p.id === params.id);
  const { addToCart } = useCart();
  if (!product) return <div>Product not found</div>;
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">{product.name}</h2>
      <div>{product.description}</div>
      <div className="font-bold">${product.price}</div>
      <button className="btn" onClick={() => addToCart(product)}>
        Add to Cart
      </button>
      <Link href="/products" className="btn ml-2">Back to Products</Link>
    </div>
  );
}