
URL = window.URL || window.webkitURL;

var gumStream;
var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext

var record_on = document.getElementById("record_on");
record_on.addEventListener("click", Record_start);

var count = 0
function Record_start() {
    count += 1
    
    if (count == 1) {
        record_on.style.backgroundColor = "#dc3545";
        var constraints = { audio: true, video:false }
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            audioContext = new AudioContext();
            gumStream = stream;
            input = audioContext.createMediaStreamSource(stream);
            rec = new Recorder(input, {numChannels:1})
            rec.record()
        })
    }
    if (count == 2) {
        count = 0
        record_on.style.backgroundColor = "#28a745";
        rec.stop();
        gumStream.getAudioTracks()[0].stop();
        rec.exportWAV(blob_create);
    }
}

function blob_create(blob) {
    // var url = URL.createObjectURL(blob);
    var filename = new Date().toISOString();
    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if(this.readyState === 4) {
           var doki = document.open("text/html", "replace");
           console.log(e.target.responseText)
            doki.write(e.target.responseText);
            doki.close();
        }
    };
    var fd = new FormData();
    fd.append("audio_data", blob, filename);
    xhr.open("POST", window.location.href, true);
    xhr.send(fd);

}