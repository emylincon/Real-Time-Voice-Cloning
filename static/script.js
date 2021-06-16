const micObj = document.querySelector('#mic');
const barObj = document.querySelector("#bar-time");
const voiceNode = document.querySelector('#voice-btn');
var myBlob = null;
function grow(){
    micObj.classList.toggle("grow");
    barObj.classList.toggle("progress-bar");
}

function loading() {
    let canvas = document.querySelector('.processing');
    canvas.innerHTML = `<div id="loading">
                    <div id="ring" class="ring">LOADING<div class='ringer'></div></div>
                </div>`;

}


function record(){
    var audio = document.getElementById( 'audio' );
    audio.innerHTML = '';
    let timeout = 7000;
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
        myBlob = blob;
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

async function sendAudioFile(file){
  const formData = new FormData();
  formData.append('audio-file', file);
  return await fetch('/audioUpload', {
    method: 'POST',
    body: formData
  });
}

function myProcess(){
    voiceNode.innerHTML = `<button style="width: 120px" class="btn" onclick="callProcess()">Process</button>`;
}

async function callProcess(){
    if(myBlob != null){
        await sendAudioFile(myBlob);
        location.replace(`/cloning`)
    }

}

async function getAudio(msg){
    const response = await fetch('/clone_api', {method: 'POST', body: JSON.stringify({'message': msg}),
        headers: {"Content-type": "application/json; charset=UTF-8"}});
    const data = await response.json();
	return data.result;
}
async function cloneVoice(){
    loading();
    let obj = document.querySelector('#msg');
    let audio = await getAudio(obj.value);
    let element = `<audio controls><source src="/${audio}" type="audio/mp3"></audio>`
    let node = document.querySelector('.processing')
    node.innerHTML = element;

}
