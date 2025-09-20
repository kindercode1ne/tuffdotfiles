const express = require("express");
const cors = require("cors");
const app = express();

// /api/validate.js
const validKeys = ["key123", "secret456", "test789", "sigmaboy124"];

module.exports = (req, res) => {
  // Vercel uses req.query for GET, req.body for POST
  const { key } = req.query;
  if (validKeys.includes(key)) {
    res.status(200).json({ valid: true });
  } else {
    res.status(200).json({ valid: false });
  }
};