import React, { useRef, useEffect } from 'react';

interface GameState {
  snake: { x: number; y: number }[];
  food: { x: number; y: number };
  score: number;
}

interface Props {
  gameState: GameState;
}

const EnvironmentVisualization: React.FC<Props> = ({ gameState }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');

    console.log('GameState in EnvironmentVisualization:', gameState); // ✅ Vérification

    if (canvas && context && gameState) {
      const tileSize = canvas.width / 10;

      // ✅ Efface le canvas avant de dessiner
      context.clearRect(0, 0, canvas.width, canvas.height);

      // ✅ Dessine le serpent
      context.fillStyle = 'green';
      gameState.snake.forEach(segment => {
        context.fillRect(segment.x * tileSize, segment.y * tileSize, tileSize, tileSize);
      });

      // ✅ Dessine la nourriture
      context.fillStyle = 'red';
      context.fillRect(
        gameState.food.x * tileSize,
        gameState.food.y * tileSize,
        tileSize,
        tileSize
      );

      // ✅ Affiche le score
      context.fillStyle = 'white';
      context.font = '20px Arial';
      context.fillText(`Score: ${gameState.score}`, 10, 30);
    } else {
      console.warn("Canvas or context not initialized"); // ✅ Vérification d'erreur
    }
  }, [gameState]); // ✅ Mise à jour à chaque changement d'état

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={400}
      style={{
        border: '2px solid #00ffcc',
        backgroundColor: '#222',
        display: 'block',
        margin: '0 auto',
        boxShadow: '0 0 20px rgba(0, 255, 204, 0.5)',
      }}
    />
  );
};

export default EnvironmentVisualization;
