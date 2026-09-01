import React,{useEffect,useRef,useState} from "react";
import ReactMarkdown from "react-markdown";
import {processVideo} from "../pose/poseProcessor";
import {landmarksToMovementData} from "../pose/landmarkAdapter";
import {analyzeMovement} from "../api";

const exercises=[
{id:"squats",name:"Squats"},
{id:"bicep_curls",name:"Bicep Curls"},
{id:"dumbbell_rows",name:"Dumbbell Rows"},
{id:"dumbbell_shoulder_press",name:"Dumbbell Shoulder Press"},
{id:"jumping_jacks",name:"Jumping Jacks"},
{id:"lateral_raises",name:"Lateral Raises"},
{id:"lunges",name:"Lunges"},
{id:"pushups",name:"Pushups"},
{id:"situps",name:"Situps"},
{id:"tricep_extensions",name:"Tricep Extensions"}
];

function MovementCoach(){
const[selectedExercise,setSelectedExercise]=useState(null);
const[inputMode,setInputMode]=useState(null);
const[videoFile,setVideoFile]=useState(null);
const[isRecording,setIsRecording]=useState(false);
const[isProcessing,setIsProcessing]=useState(false);
const[error,setError]=useState(null);
const[result,setResult]=useState(null);
const[stream,setStream]=useState(null);
const videoRef=useRef(null);
const recorderRef=useRef(null);
const chunksRef=useRef([]);

const selectedName=exercises.find(e=>e.id===selectedExercise)?.name;

useEffect(()=>()=>stopCamera(),[]);

const stopCamera=()=>{
if(recorderRef.current&&recorderRef.current.state!=="inactive")recorderRef.current.stop();
if(stream)stream.getTracks().forEach(track=>track.stop());
if(videoRef.current)videoRef.current.srcObject=null;
setStream(null);
setIsRecording(false);
};

useEffect(() => {
    if (stream && videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(() => {});
    }
}, [stream, inputMode]);

const reset=()=>{
stopCamera();
setInputMode(null);
setVideoFile(null);
setIsProcessing(false);
setError(null);
setResult(null);
};

const selectExercise=id=>{
reset();
setSelectedExercise(id);
};

const startRecording=async()=>{
setError(null);
try{
const camera=await navigator.mediaDevices.getUserMedia({video:true,audio:false});
setStream(camera);
setInputMode("camera");
if(videoRef.current)videoRef.current.srcObject=camera;
chunksRef.current=[];
const type=MediaRecorder.isTypeSupported("video/webm")?"video/webm":"";
const recorder=type?new MediaRecorder(camera,{mimeType:type}):new MediaRecorder(camera);
recorderRef.current=recorder;
recorder.ondataavailable=e=>{if(e.data.size)chunksRef.current.push(e.data);};
recorder.onstop=()=>{
const blob=new Blob(chunksRef.current,{type:recorder.mimeType||"video/webm"});
setVideoFile(new File([blob],`${selectedExercise}.webm`,{type:blob.type}));
};
recorder.start();
setIsRecording(true);
}catch(e){
setError("Camera access failed. Allow camera permission and try again.");
}
};

const stopRecording=()=>stopCamera();

const uploadVideo=e=>{
const file=e.target.files?.[0];
if(!file)return;
setVideoFile(file);
setInputMode("upload");
setError(null);
};

useEffect(()=>{
if(!videoFile||!selectedExercise)return;
let cancelled=false;
const analyze=async()=>{
setIsProcessing(true);
setError(null);
setResult(null);
try{
const poseSequence=await processVideo(videoFile);
if(!poseSequence.length)throw new Error("No pose landmarks were detected in the video.");
const movementData=landmarksToMovementData(poseSequence);
const data=await analyzeMovement(selectedExercise,movementData);
if(!cancelled)setResult(data);
}catch(e){
if(!cancelled)setError(e.message||"Movement analysis failed.");
}finally{
if(!cancelled)setIsProcessing(false);
}
};
analyze();
return()=>{cancelled=true};
},[videoFile,selectedExercise]);

return(
<main className="movement-coach">
<section className="movement-header">
<p className="eyebrow">MOVEMENT COACH</p>
<h1>Analyze your movement</h1>
<p>Select an exercise and provide a video. Processing happens locally before movement data is sent for analysis.</p>
</section>

<section className="exercise-selection">
<h2>Select an exercise</h2>
<div className="exercise-grid">
{exercises.map(exercise=>(
<button key={exercise.id} type="button" className={selectedExercise===exercise.id?"exercise-card selected":"exercise-card"} onClick={()=>selectExercise(exercise.id)}>
{exercise.name}
</button>
))}
</div>
</section>

{selectedExercise&&!inputMode&&!result&&!isProcessing&&(
<section className="analysis-start">
<p>Selected: <strong>{selectedName}</strong></p>
<div className="input-options">
<button type="button" onClick={startRecording}>Record Video</button>
<label className="upload-button">Upload Video<input type="file" accept="video/*" onChange={uploadVideo}/></label>
</div>
</section>
)}

{inputMode==="camera"&&!videoFile&&(
<section className="recording-panel">
<h2>Record {selectedName}</h2>
<video ref={videoRef} autoPlay muted playsInline className="camera-preview"/>
{isRecording&&<p>Recording...</p>}
{isRecording&&<button type="button" onClick={stopRecording}>Stop Recording</button>}
</section>
)}

{videoFile&&!isProcessing&&!result&&!error&&(
<section className="video-ready">
<p><strong>{videoFile.name}</strong></p>
<p>Your video is being prepared for local pose processing.</p>
</section>
)}

{isProcessing&&(
<section className="video-ready">
<h2>Analyzing {selectedName}</h2>
<p>Extracting pose landmarks locally and generating movement feedback...</p>
</section>
)}

{error&&(
<section className="video-ready">
<h2>Analysis failed</h2>
<p className="camera-error">{error}</p>
<button type="button" onClick={reset}>Try Another Video</button>
</section>
)}

{result&&(
<section className="analysis-results">
<h2>Movement Analysis</h2>
<div className="result-summary">
<p>Exercise: <strong>{result.exercise||selectedName}</strong></p>
<p>Repetitions: <strong>{result.repetitions??0}</strong></p>
</div>

{result.analysis?.feature_summary&&(
<div className="measurements">
<h3>Measurements</h3>
{Object.entries(result.analysis.feature_summary).map(([name,data])=>(
<div key={name} className="measurement">
<strong>{name.replaceAll("_"," ")}</strong>
<p>Min: {Number(data.min).toFixed(1)} · Max: {Number(data.max).toFixed(1)} · Range: {Number(data.range).toFixed(1)}</p>
</div>
))}
</div>
)}

{result.coaching&&(
<div className="coaching">
<h3>AI Coaching</h3>
<div className="coaching-content">
  <ReactMarkdown>{result.coaching}</ReactMarkdown>
</div>
</div>
)}

<button type="button" onClick={reset}>Analyze Another Video</button>
</section>
)}
</main>
);
}

export default MovementCoach;