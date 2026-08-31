function Navigation({ currentPage, onNavigate }) {
  return (
    <nav>
      <button onClick={() => onNavigate("home")}>
        Home
      </button>

      <button onClick={() => onNavigate("movement")}>
        Movement Coach
      </button>

      <button onClick={() => onNavigate("planner")}>
        Workout Planner
      </button>
    </nav>
  );
}

export default Navigation;