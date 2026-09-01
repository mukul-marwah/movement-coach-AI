import { FilesetResolver, PoseLandmarker } from "@mediapipe/tasks-vision";

let poseLandmarker=null;

const MODEL_PATH="https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task";
const WASM_PATH="https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm";
const MAX_PROCESSING_MS=180000;
const TARGET_INTERVAL_MS=1000/15;

export async function initializePoseLandmarker(){
if(poseLandmarker)return poseLandmarker;
const vision=await FilesetResolver.forVisionTasks(WASM_PATH);
poseLandmarker=await PoseLandmarker.createFromOptions(vision,{
baseOptions:{modelAssetPath:MODEL_PATH},
runningMode:"VIDEO",
numPoses:1,
});
return poseLandmarker;
}

export async function processVideo(videoFile){
if(!videoFile)throw new Error("No video file provided");

const start=performance.now();
const landmarker=await initializePoseLandmarker();
const videoUrl=URL.createObjectURL(videoFile);
const video=document.createElement("video");

video.src=videoUrl;
video.muted=true;
video.playsInline=true;
video.preload="auto";
video.playbackRate=1;
video.style.position="fixed";
video.style.left="0";
video.style.top="0";
video.style.width="2px";
video.style.height="2px";
video.style.opacity="0.01";
video.style.pointerEvents="none";
video.style.zIndex="-1";
document.body.appendChild(video);

const sequence=[];
let lastProcessed=-Infinity;
let finished=false;
let timeoutId=null;

try{
await new Promise((resolve,reject)=>{
video.onloadedmetadata=resolve;
video.onerror=()=>reject(new Error("Unable to load video"));
});

if(!Number.isFinite(video.duration)||video.duration<=0)throw new Error("Video has no valid duration");

const pipeline=new Promise((resolve,reject)=>{
const fail=err=>{
if(finished)return;
finished=true;
reject(err instanceof Error?err:new Error("Video processing failed"));
};

const finish=()=>{
if(finished)return;
finished=true;
resolve();
};

const frame=(now,metadata)=>{
if(finished)return;

const timestampMs=Math.max(
    Math.round(metadata.mediaTime*1000), lastProcessed+1
);

if(timestampMs-lastProcessed>=TARGET_INTERVAL_MS){
try{
const result=landmarker.detectForVideo(video,Math.round(timestampMs));
if(result.landmarks?.length){
sequence.push({
timestamp_ms:Math.round(timestampMs),
landmarks:result.landmarks[0]
});
}
lastProcessed=timestampMs;
}catch(err){
fail(err);
return;
}
}

if(!finished)video.requestVideoFrameCallback(frame);
};

video.onended=finish;
video.onerror=()=>fail(new Error("Video playback failed"));
video.requestVideoFrameCallback(frame);

video.play().catch(err=>{
if(/interrupted/i.test(err.message)){
requestAnimationFrame(()=>video.play().catch(fail));
}else{
fail(err);
}
});
});

timeoutId=setTimeout(()=>{
if(!finished){
video.pause();
finished=true;
}
},MAX_PROCESSING_MS);

await Promise.race([
pipeline,
new Promise((_,reject)=>setTimeout(()=>reject(new Error("Pose processing exceeded 30 seconds")),MAX_PROCESSING_MS))
]);

if(sequence.length<10)throw new Error(`Insufficient pose data: ${sequence.length} samples detected`);

console.log(`POSE PROCESSING TOTAL: ${((performance.now()-start)/1000).toFixed(2)}s`);
console.log(`POSE SAMPLES: ${sequence.length}`);

return sequence;
}finally{
if(timeoutId)clearTimeout(timeoutId);
video.pause();
video.remove();
URL.revokeObjectURL(videoUrl);
}
}