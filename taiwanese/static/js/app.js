//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");
var student_id = document.getElementById("student_id").getAttribute("value");
var week = document.getElementById("week").getAttribute("value");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");

    /*
        Simple constraints object, for more advanced audio features see
        https://addpipe.com/blog/audio-constraints-getusermedia/
    */

    if(document.getElementById("recordingsList").getElementsByTagName("li").length==1) {
        var old = document.getElementById("recordingsList").getElementsByTagName("li")[0]
        old.remove(old)
    }

    if(document.getElementById("success").getElementsByTagName("a").length>0) {
        var old = document.getElementById("success").getElementsByTagName("a")[0]
        old.remove(old)
    }

    var constraints = { audio: true, video:false }

    /*
        Disable the record button until we get a success or fail from getUserMedia() 
    */

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false

    /*
        We're using the standard promise based getUserMedia() 
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */
        audioContext = new AudioContext();

        //update the format 
        document.getElementById("formats").innerHTML="按下 Stop 以停止錄音"

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /* 
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        //resume
        rec.record()
        pauseButton.innerHTML="Pause";

    }
}

function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    //reset button just in case the recording is stopped while paused
    pauseButton.innerHTML="Pause";
    document.getElementById("formats").innerHTML="按下 Record 開始錄音";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    
    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}

function deleteTmpFile(fname){
    var Http = new XMLHttpRequest();
    Http.open("POST", "/homework/delete_tmp/".concat(fname));
    Http.send();
}

function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    // var link = document.createElement('a');

    //name of .wav file to use during upload and download (without extendion)
    var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //save to disk link
    // link.href = url;
    // link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
    // link.innerHTML = "Save to disk";

    //add the new audio element to li
    li.appendChild(au);

    //add the filename to the li
    // li.appendChild(document.createTextNode(filename+".wav "))

    //add the save to disk link to li
    // li.appendChild(link);

    //upload link
    var upload = document.createElement('BUTTON');
    upload.href="#";
    upload.innerHTML = "此鍵上傳";
    upload.addEventListener("click", function(event){
	  upload.innerHTML = "上傳中，請稍候";
	  upload.disabled = true;
          var xhr=new XMLHttpRequest();
          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  console.log("Server returned: ",e.target.responseText);
		  var success = document.getElementById("success");
		  var a1 = document.createElement('a');
		  a1.innerHTML='<br>上傳完成，請至<a href="/homework/summary/'.concat(student_id).concat('/"').concat('>此處</a>查看過去檔案');
		  success.appendChild(a1);
		  upload.innerHTML = "上傳完成";
              }
          };
          var fd=new FormData();
          fd.append("audio_data",blob, filename);
          xhr.open("POST","/homework/".concat(week).concat("/").concat(student_id).concat("/"), true);
          xhr.send(fd);
    })
    var b1 = document.createElement('br');
    li.appendChild(b1);
    li.appendChild(document.createTextNode ("您可以重錄數次，滿意後按 "));//add a space in between
    li.appendChild(upload)//add the upload link to li

    //add the li element to the ol
    if(document.getElementById("recordingsList").getElementsByTagName("li").length==1) {
        var old = document.getElementById("recordingsList").getElementsByTagName("li")[0]
        old.remove(old)
        recordingsList.appendChild(li);
    } else {
        recordingsList.appendChild(li);
    }

}
