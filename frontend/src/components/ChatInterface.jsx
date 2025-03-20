import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../hooks/useChat';
import { AudioRecorder } from './AudioRecorder';
import { ResponsePlayer } from './ResponsePlayer';
import { LoadingIndicator } from './LoadingIndicator';
import { MessageList } from './MessageList';
import { TranscriptBubble } from './TranscriptBubble';
import { motion, AnimatePresence } from "framer-motion";
import { 
  Send, 
  Mic, 
  Settings, 
  HelpCircle, 
  Moon, 
  Sun, 
  Volume2 
} from 'lucide-react';
import { useTheme } from '../context/AppContext';

// Animation variants
const slideInLeft = {
  hidden: { x: -100, opacity: 0 },
  visible: { 
    x: 0, 
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 15
    }
  }
};

const fadeIn = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.3 }
  }
};

const buttonHover = {
  scale: 1.05,
  transition: { duration: 0.2 }
};

export const ChatInterface = () => {
    const { messages, sendMessage, isLoading } = useChat();
    const [inputText, setInputText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [isMobile, setIsMobile] = useState(false);
    const chatContainerRef = useRef(null);
    const inputRef = useRef(null);
    const { theme, setTheme } = useTheme();

    // Check for mobile screen size
    useEffect(() => {
        const checkMobile = () => {
            setIsMobile(window.innerWidth < 768);
        };
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    // Auto-scroll effect
    useEffect(() => {
        if (chatContainerRef.current) {
            const scrollOptions = {
                top: chatContainerRef.current.scrollHeight,
                behavior: 'smooth'
            };
            chatContainerRef.current.scrollTo(scrollOptions);
        }
    }, [messages, transcript]);

    const handleTextSubmit = async (e) => {
        e.preventDefault();
        if (inputText.trim()) {
            await sendMessage({ type: 'text', content: inputText });
            setInputText('');
            inputRef.current?.focus();
        }
    };

    const handleTranscriptUpdate = (newTranscript) => {
        setTranscript(newTranscript);
    };

    const handleAudioSubmit = async (audioBlob, finalTranscript) => {
        setIsRecording(false);
        setTranscript('');
        await sendMessage({ 
            type: 'audio', 
            content: audioBlob,
            transcript: finalTranscript 
        });
    };

    // Handle textarea auto-resize
    const handleTextareaInput = (e) => {
        const textarea = e.target;
        setInputText(textarea.value);
        
        // Reset height to auto to get correct scrollHeight
        textarea.style.height = 'auto';
        
        // Set new height based on scrollHeight
        const newHeight = Math.min(textarea.scrollHeight, 200);
        textarea.style.height = `${newHeight}px`;
    };

    return (
        <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
            {/* Sidebar - Only show on desktop */}
            {!isMobile && (
                <motion.div 
                    initial="hidden"
                    animate="visible"
                    variants={slideInLeft}
                    className="hidden md:flex md:w-72 md:flex-col bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700"
                >
                    <div className="flex flex-col h-full">
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.2 }}
                            className="p-4 border-b border-gray-200 dark:border-gray-700"
                        >
                            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                                Virtual Teacher
                            </h1>
                            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                                Your AI Learning Assistant
                            </p>
                        </motion.div>
                        
                        <nav className="flex-1 p-4 space-y-2">
                            <motion.button 
                                whileHover={buttonHover}
                                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                            >
                                <HelpCircle className="w-5 h-5 mr-3" />
                                Help & FAQs
                            </motion.button>
                            <motion.button 
                                whileHover={buttonHover}
                                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                            >
                                <Settings className="w-5 h-5 mr-3" />
                                Settings
                            </motion.button>
                        </nav>

                        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                            <motion.button 
                                whileHover={buttonHover}
                                onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                            >
                                <motion.div
                                    initial={false}
                                    animate={{ rotate: theme === 'light' ? 0 : 180 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    {theme === 'light' ? (
                                        <Moon className="w-5 h-5 mr-3" />
                                    ) : (
                                        <Sun className="w-5 h-5 mr-3" />
                                    )}
                                </motion.div>
                                {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
                            </motion.button>
                        </div>
                    </div>
                </motion.div>
            )}

            {/* Main Content */}
            <div className="flex flex-col flex-1">
                {/* Messages Area */}
                <motion.div 
                    ref={chatContainerRef}
                    initial="hidden"
                    animate="visible"
                    variants={fadeIn}
                    className="flex-1 overflow-y-auto scroll-smooth"
                >
                    <MessageList messages={messages} />
                    
                    <AnimatePresence mode="wait">
                        {transcript && (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                transition={{ duration: 0.2 }}
                            >
                                <TranscriptBubble transcript={transcript} />
                            </motion.div>
                        )}

                        {isLoading && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <LoadingIndicator />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>

                {/* Input Area */}
                <motion.div 
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ type: "spring", stiffness: 100, damping: 15 }}
                    className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4"
                >
                    <div className="max-w-4xl mx-auto">
                        <div className="chat-controls">
                            <form onSubmit={handleTextSubmit} className="chat-input-form">
                                <input
                                    ref={inputRef}
                                    type="text"
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    placeholder="Type your message..."
                                    disabled={isLoading || isRecording}
                                    className="chat-input"
                                />
                                <motion.button
                                    whileHover={buttonHover}
                                    type="submit"
                                    disabled={!inputText.trim() || isLoading || isRecording}
                                    className="send-button"
                                >
                                    <Send size={18} />
                                </motion.button>
                            </form>
                            
                            <AudioRecorder
                                onRecordingComplete={handleAudioSubmit}
                                onTranscriptUpdate={handleTranscriptUpdate}
                                isDisabled={isLoading}
                            />
                        </div>
                        
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.2 }}
                            className="mt-2 text-center"
                        >
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                {isRecording ? 'Listening... (3s silence to auto-stop)' : 'Press Enter to send message, Shift + Enter for new line'}
                            </p>
                        </motion.div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};