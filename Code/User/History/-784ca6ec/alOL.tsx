import "./globals.css";
import { CartProvider } from "@/components/CartContext";
import type { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <CartProvider>
          <main className="max-w-3xl mx-auto p-4">{children}</main>
        </CartProvider>
      </body>
    </html>
  );
}
