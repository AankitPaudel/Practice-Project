// frontend/src/components/AudioRecorder.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Loader } from 'lucide-react';
import { motion } from 'framer-motion';
import { WebSocketService } from '../services/wsService';

// Get the WebSocket service instance
const wsService = new WebSocketService('ws://localhost:8000/ws');

export const AudioRecorder = ({ onRecordingComplete, onTranscriptUpdate, isDisabled }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [recordingTime, setRecordingTime] = useState(0);
    const [transcript, setTranscript] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const timerRef = useRef(null);
    const streamRef = useRef(null);
    
    // Speech recognition setup
    const recognitionRef = useRef(null);
    
    useEffect(() => {
        // Initialize WebSpeech API if available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = true;
            recognitionRef.current.interimResults = true;
            
            recognitionRef.current.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                const currentTranscript = finalTranscript || interimTranscript;
                setTranscript(currentTranscript);
                onTranscriptUpdate(currentTranscript);
            };
            
            recognitionRef.current.onerror = (event) => {
                console.error('Speech recognition error', event.error);
            };
        }
        
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.stop();
            }
        };
    }, [onTranscriptUpdate]);
    
    const startRecording = async () => {
        try {
            setIsRecording(true);
            setRecordingTime(0);
            setTranscript('');
            audioChunksRef.current = [];
            
            // Notify the server that we're starting voice recording
            wsService.startVoiceRecording();
            
            // Get microphone access
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            streamRef.current = stream;
            
            // Start speech recognition if available
            if (recognitionRef.current) {
                recognitionRef.current.start();
            }
            
            // Create media recorder
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };
            
            mediaRecorder.onstop = () => {
                // Stop speech recognition
                if (recognitionRef.current) {
                    recognitionRef.current.stop();
                }
                
                // Process the recording
                processRecording();
            };
            
            // Start recording
            mediaRecorder.start();
            
            // Start timer
            timerRef.current = setInterval(() => {
                setRecordingTime(prev => prev + 1);
            }, 1000);
            
        } catch (error) {
            console.error('Error starting recording:', error);
            setIsRecording(false);
        }
    };
    
    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            
            // Stop the timer
            if (timerRef.current) {
                clearInterval(timerRef.current);
                timerRef.current = null;
            }
            
            // Stop the stream tracks
            if (streamRef.current) {
                streamRef.current.getTracks().forEach(track => track.stop());
                streamRef.current = null;
            }
            
            setIsRecording(false);
        }
    };
    
    const processRecording = async () => {
        try {
            setIsProcessing(true);
            
            // Create audio blob
            const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
            
            // Call the callback with the audio blob and transcript
            await onRecordingComplete(audioBlob, transcript);
            
        } catch (error) {
            console.error('Error processing recording:', error);
        } finally {
            setIsProcessing(false);
            setTranscript('');
        }
    };
    
    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        return `${mins}:${secs}`;
    };
    
    return (
        <div className="audio-recorder">
            {isRecording ? (
                <div className="recording-controls">
                    <div className="recording-indicator">
                        <span className="recording-time">{formatTime(recordingTime)}</span>
                        <motion.div 
                            className="recording-dot"
                            animate={{ opacity: [1, 0.5, 1] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                        />
                    </div>
                    
                    <button 
                        className="stop-button"
                        onClick={stopRecording}
                        disabled={isProcessing}
                    >
                        <Square size={18} />
                        <span>Stop</span>
                    </button>
                </div>
            ) : (
                <button 
                    className="record-button"
                    onClick={startRecording}
                    disabled={isDisabled || isProcessing}
                >
                    {isProcessing ? (
                        <>
                            <Loader size={18} className="animate-spin" />
                            <span>Processing...</span>
                        </>
                    ) : (
                        <>
                            <Mic size={18} />
                            <span>Record</span>
                        </>
                    )}
                </button>
            )}
        </div>
    );
};

export default AudioRecorder;