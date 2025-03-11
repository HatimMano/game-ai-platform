import React, { useState } from "react";

interface GameState {
  snake: { x: number; y: number }[];
  food: { x: number; y: number };
  score: number;
}

interface Props {
  sendGameState: (state: GameState) => void;
}

const EnvironmentController: React.FC<Props> = ({ sendGameState }) => {
  const [isTrainingActive, setIsTrainingActive] = useState(false);
  const [isInferenceActive, setIsInferenceActive] = useState(false);

  // ✅ Fonction pour démarrer l'entraînement
  const handleStartTraining = async () => {
    setIsTrainingActive(true);
    setIsInferenceActive(false);
    try {
      const response = await fetch("http://localhost:8000/training/start", {
        method: "POST",
      });
      console.log(await response.json());

      console.log("📤 Sending initial game state for training");
      sendGameState({
        snake: [{ x: 0, y: 0 }],
        food: { x: 5, y: 5 },
        score: 0,
      });
    } catch (error) {
      console.error("❌ Error starting training:", error);
    }
  };

  // ✅ Fonction pour arrêter l'entraînement
  const handleStopTraining = async () => {
    setIsTrainingActive(false);
    try {
      const response = await fetch("http://localhost:8000/training/stop", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("❌ Error stopping training:", error);
    }
  };

  // ✅ Fonction pour mettre en pause l'entraînement
  const handlePauseTraining = async () => {
    try {
      const response = await fetch("http://localhost:8000/training/pause", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("❌ Error pausing training:", error);
    }
  };

  // ✅ Fonction pour sauvegarder le modèle
  const handleSaveModel = async () => {
    try {
      const response = await fetch("http://localhost:8000/training/save", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("❌ Error saving model:", error);
    }
  };

  // ✅ Fonction pour démarrer l'inférence
  const handleStartInference = async () => {
    setIsInferenceActive(true);
    setIsTrainingActive(false);
    try {
      const response = await fetch("http://localhost:8000/inference/start", {
        method: "POST",
      });
      console.log(await response.json());

      console.log("📤 Sending initial game state for inference");
      sendGameState({
        snake: [{ x: 0, y: 0 }],
        food: { x: 5, y: 5 },
        score: 0,
      });
    } catch (error) {
      console.error("❌ Error starting inference:", error);
    }
  };

  // ✅ Fonction pour arrêter l'inférence
  const handleStopInference = async () => {
    setIsInferenceActive(false);
    try {
      const response = await fetch("http://localhost:8000/inference/stop", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("❌ Error stopping inference:", error);
    }
  };

  // ✅ Fonction pour mettre en pause l'inférence
  const handlePauseInference = async () => {
    try {
      const response = await fetch("http://localhost:8000/inference/pause", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("❌ Error pausing inference:", error);
    }
  };

  return (
    <div className="controller-container">
      {/* 🎯 Bloc Training */}
      <div className={`block training ${isTrainingActive ? "active" : ""}`}>
        <h3>Training</h3>
        <button onClick={handleStartTraining} disabled={isInferenceActive}>
          Start
        </button>
        <button onClick={handleStopTraining} disabled={!isTrainingActive}>
          Stop
        </button>
        <button onClick={handlePauseTraining} disabled={!isTrainingActive}>
          Pause
        </button>
        <button onClick={handleSaveModel} disabled={!isTrainingActive}>
          Save Model
        </button>
      </div>

      {/* 🎯 Bloc Inference */}
      <div className={`block inference ${isInferenceActive ? "active" : ""}`}>
        <h3>Inference</h3>
        <button onClick={handleStartInference} disabled={isTrainingActive}>
          Start
        </button>
        <button onClick={handleStopInference} disabled={!isInferenceActive}>
          Stop
        </button>
        <button onClick={handlePauseInference} disabled={!isInferenceActive}>
          Pause
        </button>
      </div>
    </div>
  );
};

export default EnvironmentController;
