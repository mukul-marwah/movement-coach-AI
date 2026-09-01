import {useState} from "react";

const exercisePool={
bodyweight:[
{name:"Bodyweight Squats",category:"Lower Body",description:"Build lower-body strength with controlled repetitions."},
{name:"Pushups",category:"Upper Body",description:"Train your chest, shoulders, and triceps."},
{name:"Lunges",category:"Lower Body",description:"Build single-leg strength and balance."},
{name:"Glute Bridges",category:"Lower Body",description:"Develop hip and posterior-chain strength."},
{name:"Plank",category:"Core",description:"Build trunk stability and control."},
{name:"Jumping Jacks",category:"Conditioning",description:"Add simple full-body conditioning."}
],
gym:[
{name:"Squats",category:"Lower Body",description:"Build lower-body strength and movement control."},
{name:"Pushups",category:"Upper Body",description:"Train pressing strength using bodyweight."},
{name:"Dumbbell Rows",category:"Upper Body",description:"Develop controlled pulling strength."},
{name:"Dumbbell Shoulder Press",category:"Upper Body",description:"Build overhead pressing strength."},
{name:"Lunges",category:"Lower Body",description:"Develop single-leg strength and stability."},
{name:"Bicep Curls",category:"Upper Body",description:"Train controlled elbow flexion."},
{name:"Plank",category:"Core",description:"Develop core stability and control."},
{name:"Jumping Jacks",category:"Conditioning",description:"Add full-body conditioning."}
]
};

const goalLabels={
general_fitness:"General Fitness",
strength:"Build Strength",
endurance:"Improve Endurance",
movement:"Improve Movement"
};

const experienceLabels={
beginner:"Beginner",
intermediate:"Intermediate",
advanced:"Advanced"
};

function WorkoutPlanner(){
const[goal,setGoal]=useState("general_fitness");
const[experience,setExperience]=useState("beginner");
const[days,setDays]=useState(3);
const[duration,setDuration]=useState(30);
const[equipment,setEquipment]=useState("bodyweight");
const[plan,setPlan]=useState(null);

function generatePlan(){
const pool=exercisePool[equipment];
const exerciseCount=Math.min(pool.length,Math.max(4,Math.round(duration/10)));

const sets=experience==="beginner"?3:experience==="intermediate"?4:5;
const reps=goal==="strength"?"5–8":goal==="endurance"?"12–18":"8–12";
const rest=goal==="strength"?"90 sec":goal==="endurance"?"30 sec":"60 sec";

const splitNames={
2:["Full Body A","Full Body B"],
3:["Strength","Balance","Conditioning"],
4:["Upper Body","Lower Body","Upper Body","Lower Body"],
5:["Push","Pull","Legs","Upper Body","Full Body"]
};

const workouts=[];

for(let day=0;day<days;day++){
const workoutExercises=[];

for(let i=0;i<exerciseCount;i++){
const exercise=pool[(day*2+i)%pool.length];

workoutExercises.push({
...exercise,
sets:exercise.category==="Core"?"3":String(sets),
reps:exercise.category==="Core"?"30 sec":reps,
rest:exercise.category==="Core"?"45 sec":rest
});
}

workouts.push({
day:day+1,
name:splitNames[days][day],
exercises:workoutExercises
});
}

setPlan({
goal,
experience,
days,
duration,
equipment,
workouts
});
}

function resetPlan(){
setPlan(null);
}

if(plan){
return(
<main className="workout-planner">
<section className="planner-header">
<p className="eyebrow">WORKOUT PLANNER</p>
<h1>Your training plan.</h1>
<p>A structured plan based on your goals and preferences.</p>
</section>

<section className="generated-plan">
<div className="plan-overview">
<div>
<p className="eyebrow">YOUR PLAN</p>
<h2>{goalLabels[plan.goal]}</h2>
<p>{plan.days} training days · {plan.duration} minutes per session · {experienceLabels[plan.experience]}</p>
</div>

<button type="button" className="reset-plan-button" onClick={resetPlan}>
Create Another Plan
</button>
</div>

<div className="workout-list">
{plan.workouts.map(workout=>(
<section className="workout-card" key={workout.day}>
<div className="workout-card-header">
<div>
<span className="workout-day">DAY {workout.day}</span>
<h3>{workout.name}</h3>
</div>

<span className="exercise-count">
{workout.exercises.length} exercises
</span>
</div>

<div className="planned-exercises">
{workout.exercises.map((exercise,index)=>(
<div className="planned-exercise" key={`${workout.day}-${exercise.name}-${index}`}>
<div className="exercise-number">{index+1}</div>

<div className="planned-exercise-info">
<h4>{exercise.name}</h4>
<p>{exercise.description}</p>
<span>{exercise.category}</span>
</div>

<div className="exercise-prescription">
<div>
<strong>{exercise.sets}</strong>
<span>sets</span>
</div>

<div>
<strong>{exercise.reps}</strong>
<span>reps</span>
</div>

<div>
<strong>{exercise.rest}</strong>
<span>rest</span>
</div>
</div>
</div>
))}
</div>
</section>
))}
</div>

<div className="planner-note">
<h3>How to use this plan</h3>
<p>Use this as a starting structure. Prioritize controlled movement and adjust volume based on recovery.</p>
</div>
</section>
</main>
);
}

return(
<main className="workout-planner">
<section className="planner-header">
<p className="eyebrow">WORKOUT PLANNER</p>
<h1>Build your next workout.</h1>
<p>Create a structured training plan based on your goal, experience, schedule, and equipment.</p>
</section>

<section className="planner-builder">
<section className="planner-section">
<h2>What is your goal?</h2>

<div className="planner-options">
<button type="button" className={goal==="general_fitness"?"planner-option selected":"planner-option"} onClick={()=>setGoal("general_fitness")}>
<span>General Fitness</span>
<small>Build a balanced routine</small>
</button>

<button type="button" className={goal==="strength"?"planner-option selected":"planner-option"} onClick={()=>setGoal("strength")}>
<span>Build Strength</span>
<small>Focus on strength</small>
</button>

<button type="button" className={goal==="endurance"?"planner-option selected":"planner-option"} onClick={()=>setGoal("endurance")}>
<span>Improve Endurance</span>
<small>Build work capacity</small>
</button>

<button type="button" className={goal==="movement"?"planner-option selected":"planner-option"} onClick={()=>setGoal("movement")}>
<span>Improve Movement</span>
<small>Focus on control</small>
</button>
</div>
</section>

<div className="planner-two-column">
<section className="planner-section">
<h2>Experience level</h2>

<div className="planner-options compact">
{["beginner","intermediate","advanced"].map(level=>(
<button key={level} type="button" className={experience===level?"planner-option selected":"planner-option"} onClick={()=>setExperience(level)}>
<span>{experienceLabels[level]}</span>
</button>
))}
</div>
</section>

<section className="planner-section">
<h2>Available equipment</h2>

<div className="planner-options compact">
<button type="button" className={equipment==="bodyweight"?"planner-option selected":"planner-option"} onClick={()=>setEquipment("bodyweight")}>
<span>Bodyweight</span>
</button>

<button type="button" className={equipment==="gym"?"planner-option selected":"planner-option"} onClick={()=>setEquipment("gym")}>
<span>Gym Equipment</span>
</button>
</div>
</section>
</div>

<section className="planner-section">
<h2>Training schedule</h2>

<div className="planner-controls">
<label>
<span>Days per week</span>
<select value={days} onChange={e=>setDays(Number(e.target.value))}>
<option value={2}>2 days</option>
<option value={3}>3 days</option>
<option value={4}>4 days</option>
<option value={5}>5 days</option>
</select>
</label>

<label>
<span>Workout duration</span>
<select value={duration} onChange={e=>setDuration(Number(e.target.value))}>
<option value={20}>20 minutes</option>
<option value={30}>30 minutes</option>
<option value={45}>45 minutes</option>
<option value={60}>60 minutes</option>
</select>
</label>
</div>
</section>

<button type="button" className="generate-plan-button" onClick={generatePlan}>
Generate My Workout Plan
</button>
</section>
</main>
);
}

export default WorkoutPlanner;