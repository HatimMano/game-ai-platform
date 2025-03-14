import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url: string) => {
    const [states, setStates] = useState<number[][]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const socketRef = useRef<WebSocket | null>(null);


    const connect = (autoStart = false) => {
        if (socketRef.current) {
            socketRef.current.close(); // Fermer une connexion précédente s'il y en a une
        }

        socketRef.current = new WebSocket(url);

        socketRef.current.onopen = () => {
            console.log('Connected to WebSocket');
            setIsConnected(true);
            };

        if (autoStart) {
            // ✅ Utiliser un léger timeout pour s'assurer que l'état est bien mis à jour
            setTimeout(() => {
                console.log('Sending start message after reconnect');
                sendMessage({ action: 'start' });
            }, 10); // Délai minimal pour laisser `setIsConnected(true)` se propager
        }

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
        
            // 🛑 Bloquer la mise à jour si le jeu est en pause
            if (!isPaused) {
                setStates((prevStates) => [...prevStates, data.state]);
            }
        };
        

        socketRef.current.onclose = () => {
            console.log('Disconnected from WebSocket');
            setIsConnected(false);
            setStates([]);
        };

        socketRef.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    };

    useEffect(() => {
        connect(); // Établir la connexion au montage initial

        return () => {
            socketRef.current?.close(); // Fermer proprement lors du démontage
        };
    }, [url]);

    const sendMessage = (message: object) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify(message));
        }
    };

    return { states, isConnected, sendMessage, socketRef, connect, setIsPaused };
};

export default useWebSocket;