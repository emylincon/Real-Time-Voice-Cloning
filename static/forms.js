
function upload_click(){
    document.querySelector('#file').click();
}

function file_label(){
    let file = document.querySelector('#file');
    let btn = document.querySelector('.upload');
    if (file.value){
        btn.innerHTML = `<span class="material-icons">insert_photo</span>&nbsp;${file.files[0].name}`;
        btn.style.background = 'white';
        btn.style.color = 'black';
    }

}

function loading() {
    let canvas = document.querySelector('#image');
    canvas.outerHTML = `<div id="loading">
                    <div id="ring" class="ring">LOADING<div class='ringer'></div></div>
                </div>`;

}