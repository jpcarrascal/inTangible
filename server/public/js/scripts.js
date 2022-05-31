function genTokenData(projectNum) {
    let data = {};
    let hash = "0x";
    for (var i = 0; i < 64; i++) {
      hash += Math.floor(Math.random() * 16).toString(16);
    }
    data.hash = hash;
    data.tokenId = (projectNum * 1000000 + Math.floor(Math.random() * 1000)).toString();
    return data;
}
let tokenData = genTokenData(123);

//tokenData = { hash: "0x11ac16678959949c12d5410212301960fc496813cbc3495bf77aeed738579738", tokenId: "123000456" }

class Random {
  constructor() {
    this.useA = false;
    let sfc32 = function (uint128Hex) {
      let a = parseInt(uint128Hex.substr(0, 8), 16);
      let b = parseInt(uint128Hex.substr(8, 8), 16);
      let c = parseInt(uint128Hex.substr(16, 8), 16);
      let d = parseInt(uint128Hex.substr(24, 8), 16);
      return function () {
        a |= 0; b |= 0; c |= 0; d |= 0;
        let t = (((a + b) | 0) + d) | 0;
        d = (d + 1) | 0;
        a = b ^ (b >>> 9);
        b = (c + (c << 3)) | 0;
        c = (c << 21) | (c >>> 11);
        c = (c + t) | 0;
        return (t >>> 0) / 4294967296;
      };
    };
    this.prngA = new sfc32(tokenData.hash.substr(2, 32));
    this.prngB = new sfc32(tokenData.hash.substr(34, 32));
    for (let i = 0; i < 1e6; i += 2) {
      this.prngA();
      this.prngB();
    }
  }
  random_dec() {
    this.useA = !this.useA;
    return this.useA ? this.prngA() : this.prngB();
  }
  random_num(a, b) {
    return a + (b - a) * this.random_dec();
  }
  random_int(a, b) {
    return Math.floor(this.random_num(a, b + 1));
  }
  random_bool(p) {
    return this.random_dec() < p;
  }
  random_choice(list) {
    return list[this.random_int(0, list.length - 1)];
  }
}

const socket = new WebSocket('ws://localhost:8080?id=web');
const xValues = [60, 75, 90, 105, 120, 135, 150, 165, 180];
const yValues = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210];
let R = new Random();
const NUM_ROWS = 15;
const NUM_COLS = 9;
const NUM_CELLS = NUM_ROWS * NUM_COLS;
const cellId = R.random_int(0,NUM_CELLS-1);
const meta = `inTangible: ${cellId}/${NUM_CELLS}`;
const x = (cellId % NUM_COLS) * 15 + 60;
const y = Math.floor(cellId / NUM_COLS) * 15;
const c = R.random_int(0,4);
console.log(`cellid: ${cellId}`)
console.log(`x: ${x}, y: ${y}`);

socket.addEventListener('open', function (event) {
    //socket.send('Hello Server!');
    captureImage(x, y, c);
});

socket.addEventListener('image', function (event) {
    console.log('Image URL: ', event.data.url);
});

socket.addEventListener('message', function (event) {
    try {
      let message = JSON.parse(event.data);
      if(message.status = true && message.message == "image-uploaded") {
        clearInterval(timer);
        document.querySelectorAll(".cell").forEach( elem => {
          elem.style.borderColor = "#666666";
        });
        document.getElementById("output-image").setAttribute("src",message.data.url);
        document.getElementById("output-image").style.visibility = "visible";
        document.getElementById("wait-text").innerText = "Done."
        document.getElementById("output-image").classList.add("fadeIn");
        document.getElementById("controls-container").classList.add("fadeOut");
        console.log(message.source);
        var sub = meta;
        if(message.source == "cache")
          sub += " (cached)";
        setTimeout(() => {
          document.getElementById("meta").innerText = sub;
        }, 1500);
      }
    } catch {
        console.log("Response is not JSON.")
    }
    console.log('Message from server ', event.data);
});

function tableCreate() {
    const tbl = document.getElementById('controls-table');
    var k = 0;
    for (let i = 0; i < NUM_ROWS; i++) {
    //for (let i = NUM_ROWS-1; i >= 0; i--) {
      const tr = tbl.insertRow();
      for (let j = 0; j < NUM_COLS; j++) {
        const td = tr.insertCell();
        td.setAttribute("cell",`${xValues[j]};${yValues[i]}`);
        var div = document.createElement('div');
        div.setAttribute("id","cell-" + k);
        //div.appendChild(document.createTextNode(k));
        k++;
        div.classList.add("cell");
        td.appendChild(div);
        td.classList.add("pos-button");
      }
    }
}
  
tableCreate();

/*
document.querySelectorAll(".pos-button").forEach( elem => {
  elem.addEventListener("click", function() {
    tokenData = genTokenData(123);
    document.querySelectorAll(".pos-button").forEach( elem2 => {
        elem2.classList.remove("selected");
    });
    elem.classList.add("selected");
    console.log(">>> Requesting coordinates: " + elem.getAttribute("cell"));
    var x = elem.getAttribute("cell").split(";")[0];
    var y = elem.getAttribute("cell").split(";")[1];
    var c = R.random_int(0,4)
    socket.send( JSON.stringify({c: c, x: x, y: y, tid: tokenData.tokenId}) );
  });
});
*/

document.querySelector("#random").addEventListener("click", function() {
  captureImage(x, y, c);
});

function captureImage(x, y, c) {
  var message = JSON.stringify({c: c, x: x, y: y, tid: tokenData.tokenId});
  console.log(">>> Requesting: " + message);
  socket.send( message );
  document.querySelectorAll(".pos-button").forEach( elem => {
    var text = x+";"+y;
    if(elem.getAttribute("cell") == text) elem.classList.add("selected");
    else elem.classList.remove("selected");
  });
}


var index = 0;
var timer = setInterval(() => {
  document.querySelectorAll(".cell").forEach( elem => {
    elem.style.borderColor = "#666666";
  });
  document.getElementById("cell-"+index).style.borderColor = "white";
  index++;
  if(index==NUM_CELLS) index = 0;
}, 70);