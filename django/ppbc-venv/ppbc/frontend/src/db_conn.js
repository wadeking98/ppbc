// var exec = require('child_process').exec;
// var express = require("express");


// var app = express();
// app.listen(3001, ()=>{
//     console.log("server running");
// });

// app.use(express.urlencoded({extended:true}));
// app.use(express.json());


// //recieve get request
// app.get("/data", (req, res, next)=>{
//     res.json({"response":"hello"})
// });

// //recieve post data
// app.post("/data", (req, res)=>{
//   res.writeHead(200, {'Content-Type': 'text/html'});
//   console.log(req.body);

//     //send a curl to the api
//     var args = "curl -s -D - -o /dev/null -H \"Cookie: csrftoken= 00000000000000000000000000000000\"\
//      --data \"csrfmiddlewaretoken=00000000000000000000000000000000&first_name="
//      +req.body.first_name+"&last_name="
//      +req.body.last_name+"&email="
//      +req.body.email+"&password1="
//      +req.body.password1+"&password2="
//      +req.body.password2+"\" http://localhost:8000/indy/signup/";

//     exec(args, function (error, stdout, stderr) {
//       console.log('stdout: ' + stdout);
//       console.log('stderr: ' + stderr);
//       if (error !== null) {
//         console.log('exec error: ' + error);
//       }
//     });
//     res.end('hello client!');
//   });
