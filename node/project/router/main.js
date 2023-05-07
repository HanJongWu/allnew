const express = require("express")
const app = express()
const mongoose = require("mongoose")
const mysql = require("sync-mysql");
const bodyParser = require("body-parser");
const env = require("dotenv").config({ path: "../../.env"});
const query = require("async");
const { DBRef } = require("mongodb");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

var rentalSchema = mongoose.Schema({
    rentar_id: String,
    user_id: String,
    bic_id: String,
    distance: Number,
    start_time: Date,
    end_time : Date,
    start_loc: String,
    end_loc: String
})

var connection = new mysql({
  host: process.env.host,
  user: process.env.user,
  password: process.env.password,
  database: process.env.database,
});

var Rental = mongoose.model('rental', rentalSchema);

const db = mongoose.connection;

// 전체 select
app.get("/userselect", (req, res) => {
  const result = connection.query("select * from UserTbl");
//   console.log(result);
//   res.send({ 'ok': true, 'user': result});
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>User ID</th><th>Password</th><th>Name</th><th>Email</th><th>Mobile</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['User_ID']}</td>
            <td>${result[i]['Password']}</td>
            <td>${result[i]['Name']}</td>
            <td>${result[i]['Email']}</td>
            <td>${result[i]['Mobile']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
        // res.send({ 'ok': result});
});

app.get("/selectbic", (req, res) => {
  const result = connection.query("select * from BicycleTbl");
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>Bic_ID</th><th>Jurisdiction</th><th>Manager</th><th>check_status</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['Bic_ID']}</td>
            <td>${result[i]['Jurisdiction:']}</td>
            <td>${result[i]['Manager']}</td>
            <td>${result[i]['check_status']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
        // res.send({ 'ok': result});
});

app.get("/selecttr", (req, res) => {
  const result = connection.query("select * from TradeTbl");
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>시리얼 번호</th><th>유저 아이디</th><th>자전거 번호</th><th>가격</th><th>사용 시간(분)</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['Tran_ID']}</td>
            <td>${result[i]['User_ID']}</td>
            <td>${result[i]['Bic_ID']}</td>
            <td>${result[i]['Price']}</td>
            <td>${result[i]['Util_time']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
});

app.get('/list', function (req, res, next) {
    Rental.find({}, function (err, docs) {
        if (err) console.log('err')
        res.send({ 'ok': true, 'rentar': docs});
    })
})

// 부분 select
app.get("/uselectQuery", (req, res) => {
  const id = req.query.id;
  const result = connection.query("select * from UserTbl where User_ID=?", [id]);
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>User ID</th><th>Password</th><th>Name</th><th>Email</th><th>Mobile</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['User_ID']}</td>
            <td>${result[i]['Password']}</td>
            <td>${result[i]['Name']}</td>
            <td>${result[i]['Email']}</td>
            <td>${result[i]['Mobile']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
        // res.send({ 'ok': result});
});

app.get("/bselectQuery", (req, res) => {
  const id = req.query.id;
  const result = connection.query("select * from BicycleTbl where Bic_ID=?", [id]);
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>Bic ID ID</th><th>Jurisdiction</th><th>Manager</th><th>check_status</th><th>check_date</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['Bic_ID']}</td>
            <td>${result[i]['Jurisdiction:']}</td>
            <td>${result[i]['Manager']}</td>
            <td>${result[i]['check_status']}</td>
            <td>${result[i]['check_date']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
});

app.get("/yesQuery", (req, res) => {
  const id = req.query.id;
  const result = connection.query("select Bic_ID, Jurisdiction from BicycleTbl where check_status='yes'");
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>Bic ID ID</th><th>Jurisdiction</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['Bic_ID']}</td>
            <td>${result[i]['Jurisdiction']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
});

app.get("/tselectQuery", (req, res) => {
  const id = req.query.id;
  const result = connection.query("select * from TradeTbl where Tran_ID=?", [id]);
  console.log(result);
  var template = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
        </head>
        <body>
        <table border="1" style="margin:auto;">
        <thead>
            <tr><th>시리얼 번호</th><th>유저 아이디</th><th>자전거 번호</th><th>가격</th><th>사용 시간(분)</th></tr>
        </thead>
        <tbody>
        `;
        for (var i = 0; i < result.length; i++) {
            template += `
        <tr>
            <td>${result[i]['Tran_ID']}</td>
            <td>${result[i]['User_ID']}</td>
            <td>${result[i]['Bic_ID']}</td>
            <td>${result[i]['Price']}</td>
            <td>${result[i]['Util_time']}</td>
        </tr>
        `;
        }
        template += `
        </tbody>
        </table>
        </body>
        </html>
        `;
        res.send(template);
});

app.get('/findone', function (req, res, next) {
    var rentarid = req.query.input
    User.findOne({ 'rentar_id': rentarid }, function (err, doc) {
        if (err) console.log('err')
        res.send({ 'ok': true, 'rentarid': doc});
    })
})


//회원가입
app.post('/register', (req, res) => {
    const { id, pw, name, email, mobile } = req.body;
    if (id == "") {
        res.redirect('register.html')
    } else {
        let result = connection.query("select * from UserTbl where User_ID=?", [id]);
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
                        <h3 style="margin-left: 30px">Registrer Failed</h3>
                        <h4 style="margin-left: 30px">이미 존재하는 아이디입니다.</h4>
                        <a href="register.html" style="margin-left: 30px">다시 시도하기</a>
                    </div>
                </body>
                </html>
                `;
            res.end(template);
        } else {
            result = connection.query("insert into UserTbl values(?, ?, ?, ?, ?)", [id, pw, name, email, mobile]);
            console.log(result);
    
        }
    }
})

//로그인
app.post('/login', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("select * from UserTbl where User_ID=? and Password=?", [id, pw]);
    if (result.length == 0) {
        res.redirect('error.html')
    }
    if (id == 'admin' || id == 'root') {
        console.log(id + " => Administrator Logined")
        res.redirect('admin.html?id=' + id);
    } else {
        // console.log(id + " => User Logined")
        res.redirect('user.html?id=' + id)
    }

})

//반납
app.post('/return', function (req, res, next) {
    var userid = req.body.userid;
    var bicid = req.body.bicid;
    var endloc = req.body.endloc;
    const endtime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const query = connection.query("SELECT check_status FROM BicycleTbl WHERE Bic_ID = ?", [bicid]);
    console.log("1")
    if (query[0].check_status == 'yes') {
            res.redirect('error4.html')}
    
    else { 
        Rental.findOne({ 'bic_id': bicid }, function (err, rental) {
        if (err) {
            console.log('err')
            res.send({ 'ok': false})
            return;
        }
        rental.end_loc = endloc;
        rental.end_time = endtime;

        console.log(rental.start_time)
        console.log(rental.end_time)

        let srarr = rental.start_time.toISOString().slice(11, 16).replace(':', ' ').split(" ")
        let enarr = rental.end_time.toISOString().slice(11, 16).replace(':', ' ').split(" ")
        
        console.log(srarr)
        console.log(enarr)

        let hour = parseInt(enarr[0]) - parseInt(srarr[0]) 
        let mit = parseInt(enarr[1]) - parseInt(srarr[1]) 
        
        console.log(hour)
        console.log(mit)


        if (mit < 0) {
            mit += 60;
            hour--;
        }

        if (hour < 0) {
            hour += 24
        }
        
        let price =  ((hour * 60) + mit) * 10
        console.log(price)

        if (price < 1) {
            price = 1000
        }
        console.log(price)
        const utilltime = (hour * 60) + mit
        const trenid = bicid.slice(0, 5) + endtime.toString().slice(15,19);
        rental.save(function (err, silence) {
            if (err) {
                console.log('err')
                res.status(500).send('update error')
            }
            const query = connection.query("insert into TradeTbl values(?, ?, ?, ?, ?)", [trenid, userid, bicid, price, utilltime]);
            console.log(query)
            const result = connection.query("update BicycleTbl set check_status=? where Bic_ID=?", ["yes", bicid]);
            console.log(result);
            const result1 = connection.query("update BicycleTbl set jurisdiction=? where Bic_ID=?", [endloc, bicid]);
            console.log(result1);
            // res.send({ 'ok': true, 'insert': query, 'update': result})
            // res.send({ 'ok': true, 'insert': [{'trenid': trenid, 'userid': userid , 'bicid': bicid, 'price': price, 'utilltime': utilltime}]})
            res.redirect('trade.html')
        })
        
        
    })
}
})




//대여
app.post('/rental', async function (req, res, next) {
    var userid = req.body.userid;
    var bicid = req.body.bicid;
    var startloc = req.body.startloc;
    // const endtime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const starttime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const rentalid = userid.slice(0, 2) + starttime.toString().slice(15,19);
    const query = connection.query("SELECT check_status FROM BicycleTbl WHERE Bic_ID = ?", [bicid]);
    try {
        if (query[0].check_status == 'no') {
            res.redirect('error2.html')
        } else {
            var rental = new Rental({   'rentar_id': rentalid, 
                                        'user_id': userid, 
                                        'bic_id': bicid,  
                                        'start_time': starttime, 
                                        'end_time': "", 
                                        'start_loc': startloc, 
                                        'end_loc': ""      })
                rental.save(function (err, silence) {
                if (err) {
                    console.log('err')
                    res.send("error")
                    return;
                }
                const result = connection.query("update BicycleTbl set check_status=? where Bic_ID=?", ["no", bicid]);
                console.log(result);
                res.redirect('rental.html')

                // res.send({ 'ok': true, 'insert': result.affectedRows })
                // res.send({ 'ok': true, 'insert':[{"rentalid" : rentalid,"userid" : userid , 'bicid' : bicid,'start_time': starttime ,'startloc' : startloc}]})
            })
        }
    } catch (err) {
        console.log(err)
        res.redirect('user.html')
    }
});



// //거래
// app.post('/trade', async (req, res) => {
//   const { inprice, userid } = req.body;
//   try {
//     const [result] = await connection.query("SELECT User_ID, Price, from TradeTbl WHERE User_ID=?", [userid]);

//     if (result && Number(inprice) == result.Price) {
//       res.send({ 'ok': true, 'trade' : result});
//     } else {
//       res.send( "ID정보를 확인해주세요!" );
//     }
//   } catch (err) {
//     res.send( "Error!" );
//   }
// });


module.exports = app;

//거래
app.post('/trade', async (req, res) => {
    const { inprice, userid } = req.body;
    try {
      const result = connection.query("SELECT Price from TradeTbl WHERE User_ID=?", [userid]);
      console.log(result[0].Price)
      if (Number(inprice) == Number(result[0].Price)) {
          const result = connection.query("DELETE from TradeTbl WHERE User_ID=?", [userid]);
        //   res.send({ 'ok': result});
          console.log(result)
          res.redirect('index.html')
    
      } else {
      //   res.send({ 'ok': false, 'trade' : result});;
      res.send({ 'ok': false});
      }
    } catch (err) {
    // res.redirect('error3.html');
    res.redirect('error3.html');
    }
  });
  
  module.exports = app;
  
//   app.get('/delete', function (req, res, next) {
//       Rental.deleteMany({}, function (err) {
//           if (err) {
//               console.log(err);
//               res.status(500).send('delete error');
//               return;
//           }
//           res.status(200).send('삭제했습니다.');
//       });
//   });
  








//반납
// app.post('/return', async function (req, res, next) {
//     var bicid = req.body.bicid;
//     var endloc = req.body.endloc;
//     var distance = req.body.distance
//     const endtime = new Date().toISOString().slice(0, 19).replace('T', ' ');
//     const query = connection.query("SELECT check_status FROM BicycleTbl WHERE Bic_ID = ?", [bicid]);
//     var rental = new Rental({           
                                     
//                                         'bic_id': bicid, 
//                                         'distance': distance,  
//                                         'end_time': endtime, 
//                                         'end_loc': endloc     })
//     try {
//         if (query[0].check_status === 'yes') {
//             res.status(400).send("대여 기록이 없거나 이미 반납되었습니다.")
//         } else {      
//             rental.distance = distance;
//             rental.endtime = endtime;
//             rental.endloc = endloc;
//             rental.save(function (err, silence) {
//                 if (err) {
//                     console.log('err')
//                     res.status(500).send('insert error')
//                     return;
//                 }
//                 const result = connection.query("update BicycleTbl set check_status=? where Bic_ID=?", ["yes", bicid]);
//                 console.log(result);
//                 res.status(200).send("반납 완료했습니다.")
//             })
//         }
//     } catch (err) {
//         console.log(err)
//         res.status(500).send('쿼리에서 에러가 났어요 생각이 있나요?')
//     }
// })

// app.post('/insert', function (req, res, next) {
//     var rentar_id = req.body.rentar_id;
//     var user_id = req.body.user_id;
//     var bic_id = req.body.bic_id;
//     var distance = req.body.distance;
//     var start_time = req.body.start_time;
//     var end_time = req.body.end_time;
//     var start_loc = req.body.start_loc;
//     var end_loc = req.body.end_loc;
//     var rental = new Rental({   'rentar_id': rentar_id, 
//                                 'user_id': user_id, 
//                                 'bic_id': bic_id, 
//                                 'distance': distance, 
//                                 'start_time': start_time, 
//                                 'end_time': end_time, 
//                                 'start_loc': start_loc, 
//                                 'end_loc': end_loc})

//     rental.save(function (err, silence) {
//         if (err) {
//             console.log('err')
//             res.status(500).send('insert error')
//             return;
//         }
//         res.status(200).send("Inserted")
//     })
// })