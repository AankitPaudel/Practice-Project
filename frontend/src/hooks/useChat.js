// src/hooks/useChat.js
import { useState, useCallback, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { WebSocketService } from '../services/wsService';

// Create WebSocket service instance
const wsService = new WebSocketService('ws://localhost:8000/ws');

export const useChat = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const wsRef = useRef(wsService);

    // Connect to WebSocket on mount
    useEffect(() => {
        const connectWebSocket = async () => {
            try {
                await wsRef.current.connect();
                setIsConnected(true);
                console.log('WebSocket connected');
                
                // Add listener for text responses
                wsRef.current.addListener('text', (data) => {
                    setMessages(prev => [...prev, {
                        sender: 'assistant',
                        text: data.answer,
                        audioUrl: data.audio_url,
                        sources: data.sources || [],
                        confidence_score: data.confidence_score || 0.8,
                        timestamp: new Date()
                    }]);
                    setIsLoading(false);
                });
                
                // Add listener for status messages
                wsRef.current.addListener('status', (data) => {
                    console.log('Status:', data.content);
                });
                
            } catch (err) {
                console.error('WebSocket connection failed:', err);
                setError('Failed to connect to WebSocket server');
            }
        };
        
        connectWebSocket();
        
        // Cleanup on unmount
        return () => {
            wsRef.current.disconnect();
            api.cleanupAudio().catch(console.error);
        };
    }, []);

    const sendMessage = useCallback(async ({ type, content }) => {
        try {
            setIsLoading(true);
            setError(null);

            let userMessage = '';

            if (type === 'audio') {
                // First, convert audio to text
                const textResult = await api.sendAudio(content);
                userMessage = textResult.text;
                
                // Add the transcribed message to the chat immediately
                setMessages(prev => [...prev, {
                    sender: 'user',
                    text: userMessage,
                    timestamp: new Date()
                }]);

                // Use WebSocket for sending the transcribed text
                if (isConnected) {
                    wsRef.current.sendTextMessage(userMessage);
                } else {
                    // Fallback to REST API if WebSocket is not connected
                    const response = await api.sendQuestion(userMessage);
                    
                    // Add the assistant's response
                    setMessages(prev => [...prev, {
                        sender: 'assistant',
                        text: response.answer,
                        audioUrl: response.audio_url,
                        sources: response.sources,
                        confidence_score: response.confidence_score,
                        timestamp: new Date()
                    }]);
                    
                    setIsLoading(false);
                }
            } else {
                userMessage = content;
                // Add the text message to chat immediately
                setMessages(prev => [...prev, {
                    sender: 'user',
                    text: userMessage,
                    timestamp: new Date()
                }]);

                // Use WebSocket for sending text
                if (isConnected) {
                    wsRef.current.sendTextMessage(userMessage);
                } else {
                    // Fallback to REST API if WebSocket is not connected
                    const response = await api.sendQuestion(content);
                    
                    // Add the assistant's response
                    setMessages(prev => [...prev, {
                        sender: 'assistant',
                        text: response.answer,
                        audioUrl: response.audio_url,
                        sources: response.sources,
                        confidence_score: response.confidence_score,
                        timestamp: new Date()
                    }]);
                    
                    setIsLoading(false);
                }
            }

        } catch (err) {
            setError(err.message);
            console.error('Error sending message:', err);
            setIsLoading(false);
        }
    }, [isConnected]);

    return { messages, isLoading, error, sendMessage, isConnected };
};