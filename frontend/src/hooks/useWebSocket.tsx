import { useEffect, useRef, useState } from 'react';

interface GameState {
  snake: { x: number; y: number }[];
  food: { x: number; y: number };
  score: number;
}

const useWebSocket = (url: string) => {
  const socket = useRef<WebSocket | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);

  useEffect(() => {
    socket.current = new WebSocket(url);

    socket.current.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Received data:', data);
      setGameState(data);
    };

    socket.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.current.onclose = () => {
      console.log('WebSocket disconnected. Reconnecting...');
      setTimeout(() => {
        socket.current = new WebSocket(url);
      }, 1000); // Reconnexion après 1 seconde
    };

    return () => {
      socket.current?.close();
    };
  }, [url]);

  const sendGameState = (state: GameState) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      console.log("Sending game state:", state); // ✅ Vérification
      socket.current.send(JSON.stringify(state));
    }
  };
  

  return { gameState, sendGameState };
};

export default useWebSocket;
