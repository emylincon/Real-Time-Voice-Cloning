const micObj = document.querySelector('#mic');
const barObj = document.querySelector("#bar-time");
const voiceNode = document.querySelector('#voice-btn');

function grow(){
    micObj.classList.toggle("grow");
    barObj.classList.toggle("progress-bar");
}


function record(){
    var audio = document.getElementById( 'audio' );
    audio.innerHTML = '';
    let timeout = 6000;
    voiceNode.innerHTML = '';
    grow();

    var device = navigator.mediaDevices.getUserMedia({audio: true});
    var items = [];
    device.then( stream => {
    var recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e=>{
        items.push(e.data);
    if (recorder.state == 'inactive')
    {
        var blob = new Blob(items, {type: 'audio/webm'});
        var mainaudio = document.createElement('audio');
        mainaudio.setAttribute('controls', 'controls');
        audio.appendChild(mainaudio);
        mainaudio.innerHTML = '<source src="'+URL.createObjectURL(blob)+'"type="video/webm"/>';
    }
    }
    recorder.start(100);
    setTimeout(()=>{
        recorder.stop();
        grow();
        myProcess();
        }, timeout);
    })
}

function myProcess(){
    voiceNode.innerHTML = `<button style="width: 120px" onclick="callProcess()">Process</button>`;
}

function callProcess(){
    let recording = document.querySelector('source').src;
    location.replace(`/process/${recording}`)
}

async function getAudio(msg){
    const response = await fetch('/okay', {method: 'POST', body: JSON.stringify({'message': msg}),
        headers: {"Content-type": "application/json; charset=UTF-8"}});
    const data = await response.json();
	return data.result;
}

// capture Images
function capture(){
    // <canvas id="image" class="canvas"></canvas>
    let canvas = document.createElement("CANVAS");
    canvas.id = "image";
    canvas.height = 450;
    canvas.width = 500;
    let context = canvas.getContext('2d');
    let vid = document.querySelector('.videoObject');

    context.drawImage(video , 0 , 0 , 500 , 400);
    // console.log(video.height, video.width, canvas.height , canvas.width);
    vid.innerHTML = '';
    vid.appendChild(canvas);
    let img = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");  // here is the most important part because if you dont replace you will get a DOM 18 exception.
    // console.log(img);
    img_string = img;
    let change = document.querySelector('#change');
    // change.innerHTML = `<button onclick="fetchResult()">Process</button>`;
    change.innerHTML = `<a onclick="loading()" href="/process/${img}"><button>Process</button></a>`;

}
