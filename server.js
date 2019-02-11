var ps = require('python-shell')
var express = require("express");
var logfmt = require("logfmt");
var path    = require("path");
var fs = require('fs');
var multer = require('multer');
var spawn = require("child_process").spawn;
var bodyParser = require('body-parser')
var app = express();

//allow css style
app.use(express.static(__dirname));
//block all access to server.js file 
app.all('/server.js', function (req,res, next) {
   res.status(403).send({
      message: 'Access Forbidden'
   });
});
app.use('/server.js',express.static(path.join(__dirname, 'server.js')));
app.use(bodyParser.urlencoded({ extended: true })); 
//app.use(bodyParser.json());
//app.use(logfmt.requestLogger());

//fileName use as argument for python
var fileName;

const multerConfig = {
storage: multer.diskStorage({
 //Setup where the user's file will go
 destination: function(req, file, next){
   next(null, './face-recognition-opencv');
   },   
    
    //Then give the file a unique name
    filename: function(req, file, next){
        console.log(file);
        const ext = file.mimetype.split('/')[1];
        fileName = file.fieldname + '-' + Date.now() + '.'+ ext
        next(null, fileName);
      }
    }),   
    
    //A means of ensuring only images are uploaded. 
    fileFilter: function(req, file, next){
          if(!file){
          	console.log('no photo');
            next();
          }
        const image = file.mimetype.startsWith('image/');
        if(image){
          console.log('photo uploaded');
          next(null, true);
        }else{
          console.log("file not supported");
          return next();
        }
    }
};

//router
app.get('/register', function(req, res) {
   res.sendFile(path.join(__dirname+'/form.html'));
});

var upload = multer(multerConfig).single('face');
app.post('/upload',function(req,res){
  var name;
  var password;
	fs.readdir(path.join(__dirname+'/face-recognition-opencv/dataset'), function(err, items) {
    	if(items.length < 10){
    		console.log("length is " + items.length + ",can add new photo");
    		 upload(req, res, function (err) {
           name = req.body.userName;
           password = req.body.password;
           //python function here
           let options = {
             pythonPath: '/usr/local/bin/python3',
             scriptPath: path.join(__dirname+'/face-recognition-opencv'),
             args: ['--user', name, '--image', fileName]
           };
           ps.PythonShell.run('encode_faces.py', options, function (err, results) {
              if (err) throw err;
              // results is an array consisting of messages collected during execution
              console.log('results: %j', results);
           });
			    if (err) {
			         return  console.log(err);
			    } 
			  });
    		res.send('Register Complete!');
    	}
    	else{
    		console.log("length is " + items.length + ",cannot add new photo");
    		res.send('Database was full! Cannot register!');
    	}
	});
});

//port set up
var port = Number(process.env.PORT || 3000);
app.listen(port, function() {
  console.log("Listening on " + port);
});