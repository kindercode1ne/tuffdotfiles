// Hardcoded valid keys
const validKeys = ["key123", "secret456", "test789", "sigmaboy124"];

module.exports = (req, res) => {
  const { key } = req.query;
  if (validKeys.includes(key)) {
    res.status(200).json({ valid: true });
  } else {
    res.status(200).json({ valid: false });
  }
};