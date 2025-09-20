export const AUTH_KEYS = [
  "key1",
  "key2",
  "key3", // Add your keys here
];

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  // Accept key from POST body
  const { key } = req.body;

  if (AUTH_KEYS.includes(key)) {
    return res.status(200).json({ success: true, key });
  }

  return res.status(200).json({ success: false, message: "Invalid key." });
}
