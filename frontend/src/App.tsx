import React, { useState } from 'react';
import './App.css';
import EnvironmentVisualization from './components/EnvironmentVisualization';
import EnvironmentController from './components/EnvironmentController';

const App: React.FC = () => {
  const [gameState, setGameState] = useState({
    snake: [{ x: 2, y: 2 }],
    food: { x: 5, y: 5 },
    score: 0,
  });

  return (
    <div className="App">
      <h1>Snake AI Platform</h1>
      <EnvironmentVisualization gameState={gameState} />
      <EnvironmentController />
    </div>
  );
};

export default App;
