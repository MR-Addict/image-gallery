const express = require("express");

const app = express();

app.use(express.static("public"));

const port = process.env.PORT || 8085;
app.listen(port, () => console.log(`Listening on port http://localhost:${port}...`));
