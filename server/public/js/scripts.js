const socket = new WebSocket('ws://localhost:8080?id=web');

socket.addEventListener('open', function (event) {
    //socket.send('Hello Server!');
});

socket.addEventListener('image', function (event) {
    console.log('Image URL: ', event.data.url);
});

socket.addEventListener('message', function (event) {
    try {
        let message = JSON.parse(event.data);
        if(message.status = true && message.message == "image-uploaded") {
            document.getElementById("output").setAttribute("src",message.data.url);
            setCookie("imageURL", message.data.url);
        }
    } catch {
        console.log("Response is not JSON.")
    }
    console.log('Message from server ', event.data);
});

function tableCreate() {
    const tbl = document.getElementById('controls');
    tbl.style.border = '1px solid black';
    tbl.style.borderCollapse = 'collapse';
  
    for (let i = 4; i >= 0; i--) {
      const tr = tbl.insertRow();
      for (let j = 0; j < 4; j++) {
        const td = tr.insertCell();
        td.appendChild(document.createTextNode(`${j}:${i}`));
        td.style.border = '1px solid black';
        td.style.cursor = 'pointer';
        td.classList.add("pos-button");
      }
    }
}
  
tableCreate();
if(getCookie("imageURL")) {
    document.getElementById("output").setAttribute("src",getCookie("imageURL"));
}

document.querySelectorAll(".pos-button").forEach( elem => {
    elem.addEventListener("click", function() {
        document.querySelectorAll(".pos-button").forEach( elem2 => {
            elem2.classList.remove("selected");
        });
        elem.classList.add("selected");
        console.log(elem.textContent);
        socket.send(elem.textContent);
    })
});

function setCookie(name, val, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (val || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}