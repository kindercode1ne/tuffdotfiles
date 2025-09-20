// Ticket (cart/order) types and in-memory store
import type { Product } from "./products";

export type TicketStatus =
  | "pending"
  | "paid"
  | "processing"
  | "completed"
  | "cancelled";

export type Ticket = {
  id: string;
  user: string;
  items: { product: Product; quantity: number }[];
  status: TicketStatus;
  paymentMethod: string;
  messages: { from: "user" | "admin"; text: string; date: string }[];
};

// In-memory store for demo (replace with DB in production)
export const tickets: Ticket[] = [];
