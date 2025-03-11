import React, { useEffect } from 'react';
import './App.css';
import EnvironmentVisualization from './components/EnvironmentVisualization';
import EnvironmentController from './components/EnvironmentController';
import useWebSocket from './hooks/useWebSocket';

const App: React.FC = () => {
  // Définir l'URL du WebSocket
  const url = "ws://localhost:8000/ws"; 
  const { gameState, sendGameState } = useWebSocket(url);

  useEffect(() => {
    // ✅ Envoi automatique du gameState toutes les secondes
    const interval = setInterval(() => {
      if (gameState) {
        console.log('Sending game state from App:', gameState);
        sendGameState(gameState);
      }
    }, 1000); // Toutes les 1 seconde

    return () => clearInterval(interval); // Nettoyage lors du démontage du composant
  }, [gameState, sendGameState]);

  return (
    <div className="App">
      <h1>Snake AI Platform</h1>
      
      {/* 🎮 Zone d'affichage du jeu */}
      {gameState && <EnvironmentVisualization gameState={gameState} />}
      
      {/* 🕹️ Zone de contrôle */}
      <EnvironmentController sendGameState={sendGameState} />
    </div>
  );
};

export default App;
