import React, { useState } from 'react';
import EnvironmentVisualization from './components/EnvironmentVisualization';
import EnvironmentController from './components/EnvironmentController';
import useWebSocket from './hooks/useWebSocket';

const WS_URL = 'ws://localhost:8000/ws';

const App: React.FC = () => {
    const { states, isConnected, sendMessage, socketRef, connect } = useWebSocket(WS_URL);
    const [isRunning, setIsRunning] = useState(false);

    const handleStart = () => {
        if (!isRunning) {
          if (!isConnected) {
            connect(true); // 🔥 Reconnecter le WebSocket s'il est fermé
        }
          else{
          sendMessage({ action: 'start' });
          console.log('Message Start Sent')
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
            socketRef.current?.close(); // ⬅️ Fermeture explicite
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
            />
            <div>Connection status: {isConnected ? 'Connected' : 'Disconnected'}</div>
        </div>
    );
};

export default App;