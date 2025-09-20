// Simple Express API for key authentication
const express = require('express');
const app = express();
app.use(express.json());

// Hardcoded valid keys
const validKeys = [
  'key1',
  'key2',
  'key3', // Add your keys here
];

app.post('/api/auth', (req, res) => {
  const { key } = req.body;
  if (validKeys.includes(key)) {
    res.json({ valid: true });
  } else {
    res.json({ valid: false });
  }
});

module.exports = app;
