// File: frontend/src/services/api.js
const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
    async sendQuestion(question) {
        try {
            const response = await fetch(`${API_BASE_URL}/qa/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending question:', error);
            throw error;
        }
    },

    async sendAudio(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');

            const response = await fetch(`${API_BASE_URL}/audio/speech-to-text`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending audio:', error);
            throw error;
        }
    },

    async getAudioResponse(text) {
        try {
            const response = await fetch(`${API_BASE_URL}/audio/text-to-speech`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.blob();
        } catch (error) {
            console.error('Error getting audio response:', error);
            throw error;
        }
    },

    async cleanupAudio() {
        try {
            const response = await fetch(`${API_BASE_URL}/audio/cleanup`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error cleaning up audio:', error);
            throw error;
        }
    },

};