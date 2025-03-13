
import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url: string) => {
    const [state, setState] = useState<number[]>([0, 0, 0, 0]);
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
            console.log('Envoie du state')
            setState(data.state);
            console.log(data.state)

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

    return { state, isConnected, sendMessage };
};

export default useWebSocket;
