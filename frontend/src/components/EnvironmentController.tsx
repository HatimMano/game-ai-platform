import React from 'react';
import EnvironmentVisualization from './EnvironmentVisualization';

interface Props {
    // Gestion du jeu
    onStart: () => void;
    onPause: () => void;
    onStop: () => void;
    isRunning: boolean;

    // Gestion du training
    onStartTraining: () => void;
    onStopTraining: () => void;
    onSaveModel: () => void;
    isTraining: boolean;

    // Statut de connexion
    isConnected: boolean;

    // États du jeu
    states: number[][];
}

const EnvironmentController: React.FC<Props> = ({
    onStart,
    onPause,
    onStop,
    isRunning,
    onStartTraining,
    onStopTraining,
    onSaveModel,
    isTraining,
    isConnected,
    states
}) => {
    return (
        <div className="container">
            {/* ✅ Partie Inférence */}
            <div className="control-panel">
                <h1>Snake AI - Inference</h1>
                
                {/* Canvas */}
                <EnvironmentVisualization states={states} isRunning={isRunning} />

                {/* ✅ Boutons de jeu */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '16px' }}>
                    <button onClick={onStart} disabled={isRunning}>Start</button>
                    <button onClick={onPause} disabled={!isRunning}>Pause</button>
                    <button onClick={onStop} disabled={!isRunning}>Stop</button>
                </div>

                {/* ✅ Statut de connexion */}
                <div className="connection-status">
                    Status: {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
                </div>
            </div>

            {/* ✅ Séparateur */}
            <div className="separator" />

            {/* ✅ Partie Training */}
            <div className="control-panel">
                <h1>Training Status</h1>
                <div>
                    <p>Status: {isTraining ? 'Training...' : 'Idle'}</p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <button onClick={onStartTraining} disabled={isTraining}>
                        Start Training
                    </button>
                    <button onClick={onStopTraining} disabled={!isTraining}>
                        Stop Training
                    </button>
                    <button onClick={onSaveModel} disabled={!isTraining}>
                        Save Model
                    </button>
                </div>
            </div>
        </div>
    );
};

export default EnvironmentController;
