// Remove node-fetch entirely
// Just use global fetch
const express = require("express");
const { JSDOM } = require("jsdom");

const app = express();
app.use(express.static("public"));

app.get("/login", async (req, res) => {
  try {
    const response = await fetch("https://lingos.pl/h/login");
    const html = await response.text();

    const dom = new JSDOM(html);
    const document = dom.window.document;

    const form = document.querySelector("form");
    const login = form.querySelector("input[name='login']");
    const password = form.querySelector("input[name='password']");
    const button = form.querySelector("#submit-login-button");

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
  } catch (err) {
    res.send("Error: " + err.message);
  }
});

app.listen(3000, () => console.log("Running at http://localhost:3000/login"));