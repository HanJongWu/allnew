var express = require('express');
var mysql = require('mysql');
const env = require('dotenv').config({ path: "./.env" });

var connection = mysql.createConnection({
    host: process.env.host,
    user: process.env.user,
    port: process.env.port,
    password: process.env.password,
    database: process.env.database
})

var app = express();

connection.connect(function (err) {
    if (!err) {
        console.log("Database is connected....\n\n");
    } else {
        console.log("Error connecting Database....\n\n");
    }
});

app.get('/', function (req, res) {
    connection.query('select * from st_info', function (err, rows, fields) {
       // connection.end();
        if (!err) {
            // res.send(rows);
            res.writeHead(200, {'Content-Type':'text/html;charset=utf-8'});
        var template = `
		    <table border="1" margin:auto; text-align:center;>
			<tr>
				<th> ST_ID </th>
				<th> Name </th>
				<th> Dept </th>
			</tr> `;
			rows.forEach((item) => {
				template += `
				<tr>
					<th> ${item.ST_ID} </th>
					<th> ${item.NAME} </th>
					<th> ${item.DEPT} </th>
				</tr> `;
			});
			template += `</table>`;
		res.end(template);		
            console.log('The solution is : ', rows);
        } else {
            console.log('Error while performing Query');
        }
    })
})

app.listen(8000, function () {
    console.log('8000 Port : Server Started...');
})
