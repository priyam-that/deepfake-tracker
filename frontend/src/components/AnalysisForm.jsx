import React, { useState } from 'react';

const AnalysisForm = ({ onAnalyze, loading }) => {
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');

    const validateUrl = (urlString) => {
        try {
            const urlObj = new URL(urlString);
            return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
        } catch {
            return false;
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (!url.trim()) {
            setError('Please enter a URL');
            return;
        }

        if (!validateUrl(url)) {
            setError('Please enter a valid URL (must start with http:// or https://)');
            return;
        }

        onAnalyze(url);
    };

    return (
        <div className="glass-card">
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="url-input" className="form-label">
                        Enter URL to Analyze
                    </label>
                    <div className="input-wrapper">
                        <input
                            id="url-input"
                            type="text"
                            className="form-input"
                            placeholder="https://example.com/article"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            disabled={loading}
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary btn-full"
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <span className="spinner"></span>
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            Analyze URL
                        </>
                    )}
                </button>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}
            </form>
        </div>
    );
};

export default AnalysisForm;
