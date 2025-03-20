// File: frontend/src/App.jsx
import React from 'react';
import { ChatInterface } from './components/ChatInterface';
import { AppContextProvider } from './context/AppContext';
import { useAppContext } from './context/AppContext';
import './styles/main.css';

function MainContent() {
    const { theme, language } = useAppContext();
    
    return (
        <div className={`app ${theme}`}>
            <header className="app-header">
                <h1>Virtual Teacher</h1>
                <nav className="app-nav">
                    <ThemeToggle />
                    <LanguageSelector />
                </nav>
            </header>
            <main className="app-main">
                <ChatInterface />
            </main>
            <footer className="app-footer">
                <p>© 2024 Virtual Teacher. All rights reserved.</p>
            </footer>
        </div>
    );
}

function ThemeToggle() {
    const { theme, setTheme } = useAppContext();
    
    return (
        <button
            className="theme-toggle"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        >
            {theme === 'light' ? '🌙' : '☀️'}
        </button>
    );
}

function LanguageSelector() {
    const { language, setLanguage } = useAppContext();
    
    const languages = {
        en: 'English',
        es: 'Español',
        fr: 'Français',
    };
    
    return (
        <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="language-selector"
        >
            {Object.entries(languages).map(([code, name]) => (
                <option key={code} value={code}>
                    {name}
                </option>
            ))}
        </select>
    );
}

function App() {
    return (
        <AppContextProvider>
            <MainContent />
        </AppContextProvider>
    );
}

export default App;

