'use strict'

var express = require("express");
const app = express()

const HOST='0.0.0.0'
const PORT='8000'

app.get('/', (req, res) => {
<<<<<<< HEAD
	res.send('Hello World \n');
=======
<<<<<<< HEAD
    res.send('Hello World \n');
=======
	res.send('Hello World \n');
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
>>>>>>> f18a9679d25451c754f8ed8290474aa22e15adf2
});

app.listen(PORT, HOST);
console.log(`Server running at http://${HOST}:${PORT}/`);
<<<<<<< HEAD

=======
<<<<<<< HEAD
=======

>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
>>>>>>> f18a9679d25451c754f8ed8290474aa22e15adf2
