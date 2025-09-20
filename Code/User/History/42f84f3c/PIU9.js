const express = require("express");
const fetch = require("node-fetch");
const { JSDOM } = require("jsdom");

const app = express();

app.get("/login", async (req, res) => {
  const response = await fetch("https://example.com/login");
  let html = await response.text();

  const dom = new JSDOM(html);
  const document = dom.window.document;

  // Grab only the elements you want
  const form = document.querySelector("form");
  const login = form.querySelector("input[name='login']");
  const password = form.querySelector("input[name='password']");
  const button = form.querySelector("#submit-login-button");

  // Build your reskinned version
  res.send(`
    <html>
      <head><link rel="stylesheet" href="/custom.css"></head>
      <body>
        <form method="POST" action="${form.action}">
          ${login.outerHTML}
          ${password.outerHTML}
          ${button.outerHTML}
        </form>
      </body>
    </html>
  `);
});

app.listen(3000, () => console.log("Running on http://localhost:3000/login"));