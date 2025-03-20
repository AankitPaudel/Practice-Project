// src/components/MessageList.jsx
import React from 'react';
import { Message } from './Message';

export const MessageList = ({ messages }) => {
    if (messages.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[400px] p-8">
                <div className="max-w-2xl w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 text-center">
                        Welcome to Virtual Teacher! 👋
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 text-center mb-6">
                        I'm here to help you learn and understand any topic. Ask me anything!
                    </p>
                    <div className="grid gap-4 md:grid-cols-2">
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                                Try asking:
                            </h3>
                            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                                <li>"Explain quantum computing"</li>
                                <li>"How does photosynthesis work?"</li>
                                <li>"Teach me about World War II"</li>
                            </ul>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                                Features:
                            </h3>
                            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                                <li>• Voice input support</li>
                                <li>• Detailed explanations</li>
                                <li>• Real-time responses</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 p-4">
            {messages.map((message, index) => (
                <Message 
                    key={index} 
                    message={message} 
                    isLatest={index === messages.length - 1}
                />
            ))}
        </div>
    );
};

export default MessageList;