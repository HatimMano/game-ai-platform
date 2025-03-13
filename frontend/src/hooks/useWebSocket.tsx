import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url: string) => {
    const [states, setStates] = useState<number[][]>([]); // Stocke tous les états reçus
    const [isConnected, setIsConnected] = useState(false);
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        socketRef.current = new WebSocket(url);

        socketRef.current.onopen = () => {
            console.log('Connected to WebSocket');
            setIsConnected(true);
        };

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setStates((prevStates) => [...prevStates, data.state]); // Ajoute le nouvel état à la file d'attente
        };

        socketRef.current.onclose = () => {
            console.log('Disconnected from WebSocket');
            setIsConnected(false);
        };

        socketRef.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        return () => {
            socketRef.current?.close();
        };
    }, [url]);

    const sendMessage = (message: object) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify(message));
        }
    };

    return { states, isConnected, sendMessage };
};

export default useWebSocket;