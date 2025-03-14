import React, { useState } from 'react';
import EnvironmentController from './components/EnvironmentController';
import useWebSocket from './hooks/useWebSocket';

const WS_URL = 'ws://localhost:8000/ws';

const App: React.FC = () => {
    const { states, isConnected, sendMessage, socketRef, connect } = useWebSocket(WS_URL);
    const [isRunning, setIsRunning] = useState(false);
    const [isTraining, setIsTraining] = useState(false);

    const handleStart = () => {
        if (!isRunning) {
            if (!isConnected) {
                connect(true);
            } else {
                sendMessage({ action: 'start' });
            }
            setIsRunning(true);
        }
    };

    const handlePause = () => {
        if (isRunning) {
            sendMessage({ action: 'pause' });
            setIsRunning(false);
        }
    };

    const handleStop = () => {
        if (isRunning) {
            fetch('http://localhost:8000/stop-inference', { method: 'POST' });
            setIsRunning(false);
            socketRef.current?.close();
        }
    };

    const handleStartTraining = async () => {
        try {
            const response = await fetch('http://localhost:8000/start-training', {
                method: 'POST',
            });
            if (response.ok) setIsTraining(true);
        } catch (error) {
            console.error('Failed to start training:', error);
        }
    };

    const handleStopTraining = async () => {
        try {
            const response = await fetch('http://localhost:8000/stop-training', {
                method: 'POST',
            });
            if (response.ok) setIsTraining(false);
        } catch (error) {
            console.error('Failed to stop training:', error);
        }
    };

    const handleSaveModel = async () => {
        try {
            const response = await fetch('http://localhost:8000/save-model', {
                method: 'POST',
            });
            if (response.ok) console.log('Model saved');
        } catch (error) {
            console.error('Failed to save model:', error);
        }
    };

    return (
        <EnvironmentController
            onStart={handleStart}
            onPause={handlePause}
            onStop={handleStop}
            isRunning={isRunning}
            onStartTraining={handleStartTraining}
            onStopTraining={handleStopTraining}
            onSaveModel={handleSaveModel}
            isTraining={isTraining}
            isConnected={isConnected}
            states={states}
        />
    );
};

export default App;
