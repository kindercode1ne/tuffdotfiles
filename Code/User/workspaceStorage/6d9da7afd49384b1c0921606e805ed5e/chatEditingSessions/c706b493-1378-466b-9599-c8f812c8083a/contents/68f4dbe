const express = require("express");
const cors = require("cors");
const app = express();
const PORT = 3001;

// Hardcoded valid keys
const validKeys = ["key123", "secret456", "test789"];

app.use(cors());
app.use(express.json());

// Endpoint to validate key
app.get("/api/validate", (req, res) => {
  const { key } = req.query;
  if (validKeys.includes(key)) {
    res.json({ valid: true });
  } else {
    res.json({ valid: false });
  }
});

app.listen(PORT, () => {
  console.log(`Auth server running on port ${PORT}`);
});
