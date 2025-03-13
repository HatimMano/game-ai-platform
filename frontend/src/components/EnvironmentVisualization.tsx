import React, { useEffect, useRef } from 'react';

interface Props {
    state: number[]; // Format: [snake_x, snake_y, food_x, food_y]
}

const EnvironmentVisualization: React.FC<Props> = ({ state }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const gridSize = 10;
    const cellSize = 40;
    const animationRef = useRef<number | null>(null);
    const stateRef = useRef<number[]>(state); // ✅ Stockage du state dans une ref

    // ✅ Mettre à jour la référence dès que le state change
    useEffect(() => {
        stateRef.current = state;
    }, [state]);

    const drawCanvas = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // ✅ Lire directement le state depuis la ref (pas depuis le state React)
        const [snakeX, snakeY, foodX, foodY] = stateRef.current;

        // 🎯 Dessiner le serpent
        ctx.fillStyle = 'green';
        ctx.fillRect(snakeX * cellSize, snakeY * cellSize, cellSize, cellSize);

        // 🎯 Dessiner la nourriture
        ctx.fillStyle = 'red';
        ctx.fillRect(foodX * cellSize, foodY * cellSize, cellSize, cellSize);
    };

    useEffect(() => {
        const renderFrame = () => {
            drawCanvas(); // ✅ Utilise la ref au lieu du state React
            animationRef.current = requestAnimationFrame(renderFrame);
        };

        // ✅ Lancer le cycle de rendu avec requestAnimationFrame()
        animationRef.current = requestAnimationFrame(renderFrame);

        // ✅ Nettoyer le frame à la fermeture du composant
        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, []); // ✅ La boucle ne dépend pas du state (utilise la ref à la place)

    return (
        <canvas
            ref={canvasRef}
            width={gridSize * cellSize}
            height={gridSize * cellSize}
            style={{ border: '2px solid black' }}
        />
    );
};

export default EnvironmentVisualization;
