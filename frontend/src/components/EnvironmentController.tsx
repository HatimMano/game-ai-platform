import React, { useState } from "react";

const EnvironmentController: React.FC = () => {
  const [isTrainingActive, setIsTrainingActive] = useState(false);
  const [isInferenceActive, setIsInferenceActive] = useState(false);

  // 👉 Fonction pour démarrer l'entraînement
  const handleStartTraining = async () => {
    setIsTrainingActive(true);
    setIsInferenceActive(false);
    try {
      const response = await fetch("http://localhost:8000/training/start", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors du démarrage de l'entraînement :", error);
    }
  };

  // 👉 Fonction pour arrêter l'entraînement
  const handleStopTraining = async () => {
    setIsTrainingActive(false);
    try {
      const response = await fetch("http://localhost:8000/training/stop", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors de l'arrêt de l'entraînement :", error);
    }
  };

  // 👉 Fonction pour mettre en pause l'entraînement
  const handlePauseTraining = async () => {
    try {
      const response = await fetch("http://localhost:8000/training/pause", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors de la pause de l'entraînement :", error);
    }
  };

  // 👉 Fonction pour sauvegarder le modèle
  const handleSaveModel = async () => {
    try {
      const response = await fetch("http://localhost:8000/training/save", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors de la sauvegarde du modèle :", error);
    }
  };

  // 👉 Fonction pour démarrer l'inférence
  const handleStartInference = async () => {
    setIsInferenceActive(true);
    setIsTrainingActive(false);
    try {
      const response = await fetch("http://localhost:8000/inference/start", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors du démarrage de l'inférence :", error);
    }
  };

  // 👉 Fonction pour arrêter l'inférence
  const handleStopInference = async () => {
    setIsInferenceActive(false);
    try {
      const response = await fetch("http://localhost:8000/inference/stop", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors de l'arrêt de l'inférence :", error);
    }
  };

  // 👉 Fonction pour mettre en pause l'inférence
  const handlePauseInference = async () => {
    try {
      const response = await fetch("http://localhost:8000/inference/pause", {
        method: "POST",
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Erreur lors de la pause de l'inférence :", error);
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
