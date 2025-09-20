// Demo product data and types
export type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
};

export const products: Product[] = [
  {
    id: "1",
    name: "T-shirt",
    description: "High quality cotton T-shirt",
    price: 25,
  },
  { id: "2", name: "Mug", description: "Ceramic mug with logo", price: 15 },
  {
    id: "3",
    name: "Sticker Pack",
    description: "Pack of 10 stickers",
    price: 5,
  },
];
