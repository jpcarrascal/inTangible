const WebSocket = require('ws');
const url = require('url');

const wss = new WebSocket.Server({ port: 8080 });

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
    ws.send('x:2');
  } else {
    console.log("Unknown client. Disconnecting.");
    ws.send('Bye.');
    ws.terminate();
  }

});
