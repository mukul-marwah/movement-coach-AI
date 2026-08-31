import React from 'react';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import MovementCoach from './pages/MovementCoach';
import WorkoutPlanner from './pages/WorkoutPlanner';

function App() {
  const [currentPage, setCurrentPage] = React.useState('home');

  const renderPage = () => {
    if (currentPage === "movement") {
      return <MovementCoach />;
    }

    if (currentPage === "planner") {
      return <WorkoutPlanner />;
    }

    return <Home onNavigate={setCurrentPage} />;
  };

  return (
    <>
      <Navigation
        currentPage={currentPage}
        onNavigate={setCurrentPage}
      />
      {renderPage()}
    </>
  );
}

export default App;