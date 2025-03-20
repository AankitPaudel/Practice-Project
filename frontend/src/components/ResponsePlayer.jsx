// File: frontend/src/components/ResponsePlayer.jsx
import React, { useState, useRef, useEffect } from 'react';

export const ResponsePlayer = ({ audioUrl, autoPlay = false }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const audioRef = useRef(null);

    // Effect for auto-play
    useEffect(() => {
        if (audioUrl && autoPlay && audioRef.current) {
            setLoading(true);
            audioRef.current.play()
                .then(() => {
                    setLoading(false);
                    setError(null);
                })
                .catch(err => {
                    console.error('Auto-play error:', err);
                    setError('Failed to auto-play audio');
                    setLoading(false);
                });
        }
    }, [audioUrl, autoPlay]);

    // Effect to handle audio URL changes
    useEffect(() => {
        if (audioUrl) {
            setError(null);
            setLoading(true);
        }
    }, [audioUrl]);

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                setLoading(true);
                audioRef.current.play()
                    .then(() => {
                        setLoading(false);
                        setError(null);
                    })
                    .catch(err => {
                        console.error('Play error:', err);
                        setError('Failed to play audio');
                        setLoading(false);
                    });
            }
        }
    };

    const handleAudioLoaded = () => {
        setLoading(false);
        setError(null);
    };

    const handleAudioError = (e) => {
        console.error('Audio error:', e);
        setError('Error loading audio');
        setLoading(false);
    };

    return (
        <div className="audio-player">
            {error && (
                <div className="error-message text-red-500 text-sm mb-2">
                    {error}
                </div>
            )}
            <audio
                ref={audioRef}
                src={audioUrl}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
                onLoadedData={handleAudioLoaded}
                onError={handleAudioError}
                preload="auto"
            />
            <div className="flex items-center gap-2">
                <button 
                    onClick={togglePlay}
                    className={`play-button px-4 py-2 rounded-md text-white 
                        ${isPlaying 
                            ? 'bg-red-500 hover:bg-red-600' 
                            : 'bg-blue-500 hover:bg-blue-600'} 
                        disabled:opacity-50 disabled:cursor-not-allowed
                        transition duration-200`}
                    disabled={!audioUrl || error || loading}
                >
                    {loading ? 'Loading...' : isPlaying ? 'Pause' : 'Play'} Response
                </button>
                {loading && (
                    <div className="loading-spinner w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"/>
                )}
            </div>
        </div>
    );
};

export default ResponsePlayer;