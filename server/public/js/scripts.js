const socket = new WebSocket('ws://localhost:8080?id=jp');

socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

socket.addEventListener('image', function (event) {
    console.log('Image URL: ', event.data);
});

function tableCreate() {
    const body = document.body,
          tbl = document.createElement('table');
    tbl.style.width = '100px';
    tbl.style.border = '1px solid black';
    tbl.style.borderCollapse = 'collapse';
  
    for (let i = 0; i < 5; i++) {
      const tr = tbl.insertRow();
      for (let j = 0; j < 4; j++) {
        const td = tr.insertCell();
        td.appendChild(document.createTextNode(`${i}:${j}`));
        td.style.border = '1px solid black';
        td.style.cursor = 'pointer';
        td.classList.add("pos-button");
      }
    }
    body.appendChild(tbl);
}
  
tableCreate();

document.querySelectorAll(".pos-button").forEach( elem => {
    elem.addEventListener("click", function() {
        //message = JSON.stringify({ x: arr[0], y: arr[1], id: wss.getUniqueID() })
        console.log(elem.textContent);
        socket.send(elem.textContent);
    })
});

