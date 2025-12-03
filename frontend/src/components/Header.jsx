import React from 'react';

const Header = () => {
    return (
        <header className="header">
            <div className="header-logo-container">
                <img src="/deepfake-logo.svg" alt="Deepfake Tracker Logo" className="header-logo" />
                <h1 className="header-title">Deepfake AI Tracker</h1>
            </div>
            <p className="header-subtitle">
                AI-Powered Fake News & Misinformation Detection
            </p>
        </header>
    );
};

export default Header;
