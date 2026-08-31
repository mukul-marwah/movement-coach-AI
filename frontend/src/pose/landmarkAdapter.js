export function landmarksToMovementData(poseSequence){
if(!Array.isArray(poseSequence))throw new TypeError("Pose sequence must be an array");
return poseSequence.map(frame=>frame.landmarks.map(l=>[
l.x,
l.y,
l.z,
l.visibility??0
]));
}