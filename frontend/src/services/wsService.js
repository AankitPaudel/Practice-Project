// File: frontend/src/services/wsService.js
export class WebSocketService {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.listeners = new Map();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.notifyListeners(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        return new Promise((resolve, reject) => {
            this.ws.onopen = () => resolve();
            this.ws.onerror = () => reject();
        });
    }

    addListener(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        this.listeners.get(event).add(callback);
    }

    removeListener(event, callback) {
        const callbacks = this.listeners.get(event);
        if (callbacks) {
            callbacks.delete(callback);
        }
    }

    notifyListeners(data) {
        const callbacks = this.listeners.get(data.type);
        if (callbacks) {
            callbacks.forEach(callback => callback(data));
        }
    }
    
    sendTextMessage(text) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            const message = {
                type: "text_input",
                content: text
            };
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not connected');
        }
    }
    
    startVoiceRecording() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            const message = {
                type: "start_voice_recording"
            };
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not connected');
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}