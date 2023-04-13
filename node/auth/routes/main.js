const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("sync-mysql");
const env = require("dotenv").config({ path: "../../.env" });

var connection = new mysql({
  host: process.env.host,
  user: process.env.user,
  password: process.env.password,
  database: process.env.database,
});

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/hello", (req, res) => {
  res.send("관리지 접속중입니다.");
});

app.post("/login", (req, res) => {
  const { id, pw } = req.body;
  const result = connection.query(
    "select * from user where userid=? and passwd=?",
    [id, pw]
  );
  if (result.length == 0) {
    res.redirect("error.html");
  }
  if (id == "admin" || id == "root") {
    console.log(id + " => Administrator Logined");
    res.redirect("member.html");
  } else {
    console.log(id + " => User Logined");
    res.redirect("main.html");
  }
});

app.post("/register", (req, res) => {
  const { id, pw } = req.body;
  if (id == "") {
    res.redirect("register.html");
  } else {
    let result = connection.query("select * from user where userid=?", [id]);
    if (result.length > 0) {
      res.writeHead(200);
      var template = `
        <!doctype html>
        <html>
        <head>
            <title>Error</title>
            <meta charset="utf-8">
        </head>
        <body>
            <div>
              <h3 style="margin-left: 30px">Register Failed</h3>
              <h4 style="margin-left: 30px">이미 존재하는 아이디입니다.<h4>
              <a href="register.html" style="margin-left: 30px">다시 시도하기</a>
            <div>
        <body>
        </html>
       `;
      res.end(template);
    } else {
      result = connection.query("insert into user values (?,?)", [id, pw]);
      console.log(result);
      res.redirect("/");
    }
  }
});

app.get("/select", (req, res) => {
  const result = connection.query("select * from user");
  console.log(result);
  res.send(result);
});

app.post("/select", (req, res) => {
  const result = connection.query("select * from user");
  console.log(result);
  res.send(result);
});

app.get("/selectQuery", (req, res) => {
  const id = req.query.id;
  const result = connection.query("select * from user where userid=?", [id]);
  console.log(result);
  res.send(result);
});

app.post("/selectQuery", (req, res) => {
  const id = req.body.id;
  const result = connection.query("select * from user where userid=?", [id]);
  console.log(result);
  res.send(result);
});

app.post("/insert", (req, res) => {
  const { id, pw } = req.body;
  const result = connection.query("insert into user values (?, ?)", [id, pw]);
  console.log(result);
  res.redirect("/selectQuery?id=" + req.body.id);
});

app.post("/update", (req, res) => {
  const { id, pw } = req.body;
  const result = connection.query("update user set passwd=? where userid=?", [
    pw,
    id,
  ]);
  console.log(result);
  res.redirect("/selectQuery?id=" + req.body.id);
});

app.post("/delete", (req, res) => {
  const id = req.body.id;
  const result = connection.query("delete from user where userid=?", [id]);
  console.log(result);
  res.redirect("/select");
});

module.exports = app;
