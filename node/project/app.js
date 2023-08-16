const express = require('express')
const morgan = require('morgan')
const path = require('path')
const app = express()
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')

app.set('port', process.env.PORT || 8000)
app.use(morgan('dev'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())
app.use(express.static(path.join(__dirname, 'public')))

const mongoose = require("mongoose")
mongoose.connect("mongodb://43.201.231.90:27017/test")

// const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env"});

var main = require('./router/main.js')
app.use('/', main)

app.listen(app.get('port'), () => {
    console.log('8000 Port : Server Started…')
});