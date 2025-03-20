// src/components/Message.jsx
import React from 'react';
import { ResponsePlayer } from './ResponsePlayer';
import { User, Bot } from 'lucide-react';

export const Message = ({ message, isLatest }) => {
    const isUser = message.sender === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} gap-3 mx-4`}>
            {!isUser && (
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-white" />
                </div>
            )}
            
            <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[80%]`}>
                <div className={`px-4 py-2 rounded-2xl ${
                    isUser 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
                }`}>
                    <div className="text-sm whitespace-pre-wrap">{message.text}</div>
                </div>
                
                {message.audioUrl && (
                    <div className="mt-2">
                        <ResponsePlayer 
                            audioUrl={message.audioUrl}
                            autoPlay={isLatest}
                        />
                    </div>
                )}
            </div>

            {isUser && (
                <div className="flex-shrink-0 w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </div>
            )}
        </div>
    );
};

export default Message;