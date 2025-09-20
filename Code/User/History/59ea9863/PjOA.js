export const AUTH_KEYS = [
  "dev-key-cwel",
  "v4k7zp-m9q2hd-s6t3lx",
  "n2r8jw-t7z5kc-q4m9vp",
  "h6d3zt-v8x2rl-m7p5qk",
  "j9m2hs-t4b6zn-w3q7kp",
  "p8x3rn-k2m9vh-d6j7qt",
  "q7l2kd-m8v5jr-w9h3tp",
  "f4b9zx-t1p6kn-r7m8hq",
  "t6q3vn-h9k2zr-p5j8wm",
  "w7r2lp-q3m9tk-v6h5dz",
  "z2h8nj-p7m3kd-w4q9vx",
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
