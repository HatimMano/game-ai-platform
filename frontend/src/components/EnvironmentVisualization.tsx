import React, { useEffect, useRef } from 'react';

interface Props {
    states: number[][]; // Reçoit tous les états
}

const EnvironmentVisualization: React.FC<Props> = ({ states }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const gridSize = 10;
    const cellSize = 40;
    const animationRef = useRef<number | null>(null);
    const currentStateIndexRef = useRef<number>(0); // Index de l'état actuel à afficher

    const drawCanvas = (state: number[]) => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const [snakeX, snakeY, foodX, foodY] = state;

        // Dessiner le serpent
        ctx.fillStyle = 'green';
        ctx.fillRect(snakeX * cellSize, snakeY * cellSize, cellSize, cellSize);

        // Dessiner la nourriture
        ctx.fillStyle = 'red';
        ctx.fillRect(foodX * cellSize, foodY * cellSize, cellSize, cellSize);
    };

    useEffect(() => {
        const renderFrame = () => {
            if (states.length > 0 && currentStateIndexRef.current < states.length) {
                drawCanvas(states[currentStateIndexRef.current]);
                currentStateIndexRef.current += 1; // Passe à l'état suivant
            }
            animationRef.current = requestAnimationFrame(renderFrame);
        };

        animationRef.current = requestAnimationFrame(renderFrame);

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [states]);

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