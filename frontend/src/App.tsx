import React, { useState } from 'react';
import EnvironmentVisualization from './components/EnvironmentVisualization';
import EnvironmentController from './components/EnvironmentController';
import useWebSocket from './hooks/useWebSocket';

const WS_URL = 'ws://localhost:8000/ws';

const App: React.FC = () => {
    const { states, isConnected, sendMessage, socketRef, connect } = useWebSocket(WS_URL);
    const [isRunning, setIsRunning] = useState(false);
    const [isTraining, setIsTraining] = useState(false);

    // ⭐ Start Game
    const handleStart = () => {
        if (!isRunning) {
            if (!isConnected) {
                connect(true);
            } else {
                sendMessage({ action: 'start' });
                console.log('Message Start Sent');
            }
            setIsRunning(true);
        }
    };

    // ⭐ Pause Game
    const handlePause = () => {
        if (isRunning) {
            sendMessage({ action: 'pause' });
            setIsRunning(false);
        }
    };

    // ⭐ Stop Game
    const handleStop = () => {
        if (isRunning) {
            fetch('http://localhost:8000/stop-inference', { method: 'POST' });
            setIsRunning(false);
            socketRef.current?.close();
        }
    };

    // ⭐ Start Training
    const handleStartTraining = async () => {
        try {
            const response = await fetch('http://localhost:8000/start-training', {
                method: 'POST',
            });
            if (response.ok) {
                console.log('Training started');
                setIsTraining(true);
            }
        } catch (error) {
            console.error('Failed to start training:', error);
        }
    };

    // ⭐ Stop Training
    const handleStopTraining = async () => {
        try {
            const response = await fetch('http://localhost:8000/stop-training', {
                method: 'POST',
            });
            if (response.ok) {
                console.log('Training stopped');
                setIsTraining(false);
            }
        } catch (error) {
            console.error('Failed to stop training:', error);
        }
    };

    // ⭐ Save Model
    const handleSaveModel = async () => {
        try {
            const response = await fetch('http://localhost:8000/save-model', {
                method: 'POST',
            });
            if (response.ok) {
                console.log('Model saved');
            }
        } catch (error) {
            console.error('Failed to save model:', error);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
            <h1>Snake AI</h1>
            <EnvironmentVisualization states={states} isRunning={isRunning} />
            <EnvironmentController
                onStart={handleStart}
                onPause={handlePause}
                onStop={handleStop}
                isRunning={isRunning}
                onStartTraining={handleStartTraining}
                onStopTraining={handleStopTraining}
                onSaveModel={handleSaveModel}
                isTraining={isTraining}
            />
            <div>Connection status: {isConnected ? 'Connected' : 'Disconnected'}</div>
        </div>
    );
};

export default App;
