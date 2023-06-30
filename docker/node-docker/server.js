'use strict'

var express = require("express");
const app = express()

const HOST='0.0.0.0'
const PORT='8000'

app.get('/', (req, res) => {
<<<<<<< HEAD
    res.send('Hello World \n');
=======
	res.send('Hello World \n');
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
});

app.listen(PORT, HOST);
console.log(`Server running at http://${HOST}:${PORT}/`);
<<<<<<< HEAD
=======

>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
