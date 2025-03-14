import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url: string) => {
    const [states, setStates] = useState<number[][]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const socketRef = useRef<WebSocket | null>(null);

    const connect = (autoStart = false) => {
        if (socketRef.current) {
            socketRef.current.close();
        }

        socketRef.current = new WebSocket(url);

        socketRef.current.onopen = () => {
            console.log('✅ Connected to WebSocket');
            setIsConnected(true);
            if (autoStart) {
                setTimeout(() => {
                    sendMessage({ action: 'start' });
                }, 10);
            }
        };

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (!isPaused) {
                setStates((prevStates) => [...prevStates, data.state]);
            }
        };

        socketRef.current.onclose = () => {
            console.log('🔴 Disconnected from WebSocket');
            setIsConnected(false);
            setStates([]);
        };

        socketRef.current.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
        };
    };

    useEffect(() => {
        connect();

        return () => {
            socketRef.current?.close();
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