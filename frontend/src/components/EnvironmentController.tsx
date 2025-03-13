import React from 'react';

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
}) => {
    return (
        <div style={{ display: 'flex', gap: '10px', marginTop: '20px', flexWrap: 'wrap' }}>
            {/* Boutons pour le jeu */}
            <button onClick={onStart} disabled={isRunning}>Start</button>
            <button onClick={onPause} disabled={!isRunning}>Pause</button>
            <button onClick={onStop} disabled={!isRunning}>Stop</button>

            {/* Boutons pour le training */}
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
    );
};

export default EnvironmentController;
