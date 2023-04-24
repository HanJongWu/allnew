const { connect } = require("http2");
const mysql = require("mysql2/promise");
const env = require("dotenv").config({path: "../../.env"});

const db = async () => {
    try {
        //db connection
        let connection = await mysql.createConnection({
            host: process.env.host,
            user: process.env.user,
            password: process.env.password,
            database: process.env.database
        });
    
        let [rows, fields] = await connection.query("select * from st_info");
        console.log(rows);
    
        let data = {
            st_id: "202399",
            name: "Han",
            dept: "Computer"
        }

        // insert query
        let [results] = await connection.query("insert into st_info set ?", data);
        console.log("data is Inserted~!!")

        let unsertId = data.st_id;

        // select query of inserted data
        [rows, fields] = await connection.query("select * form st_info where st_id = ?", insertId);
        console.log(rows);

        // update query
        [results] = await connection.query("update st_info set dept = ? where st_id = ? ", insertId);
        
        // select query of inserted data
        [rows, fields] = await connection.query("select * form st_info where st_id = ?", insertId);
        console.log(rows);

        // delete row
        [rows, fields] = await connection.query("delete * form st_info where st_id = ?", insertId);
        console.log(rows);

        // select query all data
        [rows, fields] = await connection.query("select * form st_info");
        console.log(rows);

    } catch (error) {
        console.log(error);
    }
};

db();