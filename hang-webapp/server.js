const express = require('express');
const path = require('path');
const app = express();

app.use(express.static( __dirname + '/dist' ));

PORT = process.env.PORT || 4200;
app.listen(PORT);

// path location strategy for Angular Routing
app.get('/*', (req, res) => {res.sendFile(path.join(__dirname + '/dist/index.html'))});

console.log(`App is running!\nListening on port ${PORT}`)
