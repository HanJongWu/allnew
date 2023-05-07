const axios = require('axios');

axios 
    .post('http://192.168.1.28:8000/todos', {
        todo: "Buy the milk"
    })
    .then(res=> {
        console.log(`statusCode : ${res.status}`)
        console.log(res)
    })
    .catch(error => {
        console.log(error)
    })