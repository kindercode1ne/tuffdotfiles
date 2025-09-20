const express = require("express");
const cors = require("cors");
const app = express();

// Hardcoded valid keys
const validKeys = ["key123", "secret456", "test789", "sigmaboy124"];

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

// Export the app for Vercel serverless function
module.exports = app;
