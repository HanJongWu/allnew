'use strict';

var http = require("http");
var server = http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type':'text/plain'});
    res.end('Hello World\n');
}).listen(8000, '0.0.0.0');

console.log('Server Started...');

var signals = {
    'SIGINT':2,
    'SIGTERM':15
};

function shutdown(signal, value) {
    server.close(function() {
        console.log('Server Stopped by ' + signal);
        process.exit(128 + value);
    })
}

Object.keys(signals).forEach(function (signal) {
    process.on(signal, function () {
        shutdown(signal, signals[signal]);
    });
});
