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


const wss = new WebSocket.Server({ server });

wss.getUniqueID = function () {
  function s4() {
      return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }
  return s4() + s4() + '-' + s4();
};

wss.on('connection', (ws, req) => {

  ws.on('message', message => {
    console.log(`Received message => ${message}`);
  });
  const parameters = url.parse(req.url, true);
  if(parameters.query.id && parameters.query.id == "jp") {
    console.log(parameters.query.id);
    ws.uid = wss.getUniqueID();
    ws.send('Welcome ' + parameters.query.id + ". UID: " + ws.uid);
    let message = JSON.stringify({ x: 2, y: 3, id: wss.getUniqueID() })
    ws.send(message);
  } else {
    console.log("Unknown client. Disconnecting.");
    ws.send('Bye.');
    ws.terminate();
  }

});

/* ------------------------ */

// From: https://attacomsian.com/blog/uploading-files-nodejs-express
app.post('/upload-image', async (req, res) => {
  console.log("Got file upload request...");
  try {
      if(!req.files) {
          res.send({
              status: false,
              message: 'No file uploaded'
          });
          console.log(req.files);
      } else {
          let image = req.files.image;
          image.mv('./cache/' + image.name);
          res.send({
              status: true,
              message: 'File is uploaded',
              data: {
                  name: image.name,
                  mimetype: image.mimetype,
                  size: image.size
              }
          });
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