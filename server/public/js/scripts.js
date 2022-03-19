const socket = new WebSocket('ws://localhost:8080?id=web');

socket.addEventListener('open', function (event) {
    //socket.send('Hello Server!');
});

socket.addEventListener('image', function (event) {
    console.log('Image URL: ', event.data);
});

socket.addEventListener('message', function (event) {
    try {
        let message = JSON.parse(event.data);
        if(message.status = true && message.message == "image-uploaded") {
            document.getElementById("output").setAttribute("src",message.data.url);
        }
    } catch {
        console.log("Response is not JSON.")
    }
    console.log('Message from server ', event.data);
});

function tableCreate() {
    const tbl = document.getElementById('controls');
    tbl.style.width = '100px';
    tbl.style.border = '1px solid black';
    tbl.style.borderCollapse = 'collapse';
  
    for (let i = 5; i >= 0; i--) {
      const tr = tbl.insertRow();
      for (let j = 0; j < 4; j++) {
        const td = tr.insertCell();
        td.appendChild(document.createTextNode(`${i}:${j}`));
        td.style.border = '1px solid black';
        td.style.cursor = 'pointer';
        td.classList.add("pos-button");
      }
    }
    var css = 'table td:hover{ background-color: #44ff44; }';
    var style = document.createElement('style');
    if (style.styleSheet) {
        style.styleSheet.cssText = css;
    } else {
        style.appendChild(document.createTextNode(css));
    }
    document.getElementsByTagName('head')[0].appendChild(style);
}
  
tableCreate();

document.querySelectorAll(".pos-button").forEach( elem => {
    elem.addEventListener("click", function() {
        //message = JSON.stringify({ x: arr[0], y: arr[1], id: wss.getUniqueID() })
        console.log(elem.textContent);
        socket.send(elem.textContent);
    })
});

