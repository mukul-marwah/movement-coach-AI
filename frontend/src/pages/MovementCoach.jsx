import React, { useState } from "react";

const exercises = [
{ id: "squats", name: "Squats" },
{ id: "bicep_curls", name: "Bicep Curls" },
{ id: "dumbbell_rows", name: "Dumbbell Rows" },
{ id: "dumbbell_shoulder_press", name: "Dumbbell Shoulder Press" },
{ id: "jumping_jacks", name: "Jumping Jacks" },
{ id: "lateral_raises", name: "Lateral Raises" },
{ id: "lunges", name: "Lunges" },
{ id: "pushups", name: "Pushups" },
{ id: "situps", name: "Situps" },
{ id: "tricep_extensions", name: "Tricep Extensions" },
];

function MovementCoach() {
const [selectedExercise, setSelectedExercise] = useState(null);
const [analysisStarted, setAnalysisStarted] = useState(false);

const selectedExerciseName =
exercises.find((exercise) => exercise.id === selectedExercise)?.name;

const handleExerciseSelect = (exerciseId) => {
setSelectedExercise(exerciseId);
setAnalysisStarted(false);
};

const handleStartAnalysis = () => {
if (selectedExercise === null) {
return;
}

setAnalysisStarted(true);

};

return (
<main className="movement-coach">
<section className="movement-header">
<p className="eyebrow">MOVEMENT COACH</p>

    <h1>Analyze your movement</h1>

    <p>
      Select an exercise to begin a movement analysis.
    </p>
  </section>

  <section className="exercise-selection">
    <h2>Select an exercise</h2>

    <div className="exercise-grid">
      {exercises.map((exercise) => (
        <button
          key={exercise.id}
          type="button"
          className={
            selectedExercise === exercise.id
              ? "exercise-card selected"
              : "exercise-card"
          }
          onClick={() => handleExerciseSelect(exercise.id)}
        >
          {exercise.name}
        </button>
      ))}
    </div>
  </section>

  <section className="analysis-start">
    <p>
      Selected: <strong>{selectedExerciseName || "None"}</strong>
    </p>

    <button
      type="button"
      onClick={handleStartAnalysis}
    >
      Start Analysis
    </button>

    {analysisStarted && (
      <p>
        Analysis ready to begin for{" "}
        <strong>{selectedExerciseName}</strong>.
      </p>
    )}
  </section>
</main>

);
}

export default MovementCoach;