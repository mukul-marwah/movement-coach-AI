import { useState } from "react";
import { checkBackend } from "../api";

function Home({ onNavigate }) {
  const [backendStatus, setBackendStatus] = useState("Not checked");

  const testBackend = async () => {
    try {
      const result = await checkBackend();
      setBackendStatus(result.status);
    } catch (error) {
      setBackendStatus("Backend unavailable");
      console.error(error);
    }
  };
  return (
    <main className="home">
      <section className="hero">
        <p className="eyebrow">MOVEMENT COACH AI</p>

        <h1>
          Visual movement coaching
          <br />
          powered by AI.
        </h1>

        <p className="hero-text">
          Analyze movement with visual data and receive
          measurement-based coaching feedback.
        </p>

        <div className="home-actions">
          <button onClick={() => onNavigate("movement")}>
            Movement Coach
          </button>

          <button onClick={() => onNavigate("planner")}>
            Workout Planner
          </button>
        </div>
      </section>

      <section className="features">
        <div>
          <h2>Movement Analysis</h2>
          <p>
            Analyze movement data and identify measurable
            patterns across an exercise.
          </p>
        </div>
        <div>
          <h2>Personalized Planning</h2>
          <p>
            Generate structured workout plans based on
            your preferences and goals.
          </p>
        </div>

        <div>
          <h2>Privacy First</h2>
          <p>
            Movement processing is designed around keeping
            raw movement data on the user's device.
          </p>
        </div>
      </section>
    </main>
  );
}

export default Home;