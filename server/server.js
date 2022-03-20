const WebSocket = require('ws');
const url = require('url');
const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const fileUpload = require('express-fileupload');
const cors = require('cors');
const bodyParser = require('body-parser');

app.use(fileUpload({
  createParentPath: true
}));

//add other middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use('/js', express.static(__dirname + '/public/js/'));
app.use('/css', express.static(__dirname + '/public/css/'));
app.use('/images', express.static(__dirname + '/public/images/'));
app.use('/cache', express.static(__dirname + '/public/cache/'));

const wss = new WebSocket.Server({ server });

wss.getUniqueID = function () {
  function s4() {
      return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }
  return s4() + s4() + '-' + s4();
};


let web;
let pi;
wss.on('connection', (ws, req) => {
  const parameters = url.parse(req.url, true);
  ws.uid = wss.getUniqueID();
  if(parameters.query.id == "pi" || parameters.query.id == "web") {
    //ws.send( JSON.stringify('Welcome ' + parameters.query.id + ". UID: " + ws.uid) );
    if(parameters.query.id == "web") web = ws;
    else pi = ws;
  } else {
    console.log("Unknown client. Disconnecting.");
    ws.send('Bye.');
    ws.terminate();
  }

  if(web) {
    web.on('message', message => {
      console.log(`Received message => ${message}`);
      let arr = message.toString().split(":").map(x => parseInt(x));
      let command = JSON.stringify({ x: arr[0], y: arr[1], id: wss.getUniqueID() });
      console.log("Sending to Pi: " + command);
      pi.send(command);
    });
  }

});

/* ------------------------ */

// From: https://attacomsian.com/blog/uploading-files-nodejs-express
app.post('/upload-image', async (req, res) => {
  try {
      if(!req.files) {
          res.send({
              status: false,
              message: 'No file uploaded'
          });
          console.log(req.files);
      } else {
          // Send URL to web app:
          console.log("Image uploaded");
          let image = req.files.image;
          image.mv('./public/cache/' + image.name);
          let response = JSON.stringify({
              status: true,
              message: 'image-uploaded',
              data: {
                  name: image.name,
                  mimetype: image.mimetype,
                  size: image.size,
                  url: "/cache/" + image.name
              }
          });
          web.send(response);
      }
  } catch (err) {
      res.status(500).send(err);
  }
});

app.get('/', (req, res) => {
  var page = '/public/index.html';
  res.sendFile(__dirname + page);
});

var port = process.env.PORT || 8080;
server.listen(port, () => {
  console.log('listening on *:' + port);
});