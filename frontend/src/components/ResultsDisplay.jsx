import React from 'react';

const ResultsDisplay = ({ results }) => {
    if (!results) return null;

    const { credibility_score, warning, analysis, key_findings, title, domain } = results;

    // Calculate percentage for circular progress
    const scorePercentage = `${credibility_score}%`;

    return (
        <div className="results-container">
            <div className="glass-card">
                {/* Score Display */}
                <div className="score-display">
                    <div className="score-circle" style={{ '--score-percentage': scorePercentage }}>
                        <div className="score-circle-bg"></div>
                        <div className="score-circle-inner">
                            <div className="score-value">{credibility_score}</div>
                            <div className="score-label">Score</div>
                        </div>
                    </div>

                    {/* Warning Badge */}
                    <div className="text-center">
                        <span className={`warning-badge ${warning.level}`}>
                            {warning.level === 'safe' && '✓'}
                            {warning.level === 'suspicious' && '⚠'}
                            {warning.level === 'dangerous' && '⚠'}
                            {' '}
                            {warning.label}
                        </span>
                        <p className="mb-lg" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--spacing-sm)' }}>
                            {warning.message}
                        </p>
                    </div>
                </div>

                {/* Article Info */}
                <div className="mb-lg" style={{
                    padding: 'var(--spacing-md)',
                    background: 'var(--color-bg-secondary)',
                    borderRadius: 'var(--radius-md)',
                    borderLeft: '3px solid var(--color-accent-primary)'
                }}>
                    <div style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 'var(--spacing-xs)' }}>
                        Source: {domain}
                    </div>
                    <div style={{ fontSize: '1rem', color: 'var(--color-text-primary)', fontWeight: '500' }}>
                        {title}
                    </div>
                </div>

                {/* Analysis Grid */}
                <div className="analysis-grid">
                    {/* Source Credibility */}
                    <div className="analysis-item">
                        <div className="analysis-item-title">Source Credibility</div>
                        <div className="analysis-item-value">{analysis.source_credibility.score}/100</div>
                        <div className="analysis-item-description">
                            {analysis.source_credibility.classification}
                            <br />
                            <small>{analysis.source_credibility.note}</small>
                        </div>
                    </div>

                    {/* Clickbait Score */}
                    <div className="analysis-item">
                        <div className="analysis-item-title">Clickbait Detection</div>
                        <div className="analysis-item-value" style={{
                            color: analysis.clickbait.score > 50 ? 'var(--color-danger)' : 'var(--color-success)'
                        }}>
                            {analysis.clickbait.score}/100
                        </div>
                        <div className="analysis-item-description">
                            {analysis.clickbait.score > 50 ? 'High clickbait indicators' : 'Low clickbait indicators'}
                            {analysis.clickbait.indicators.length > 0 && (
                                <div style={{ marginTop: 'var(--spacing-xs)', fontSize: '0.75rem' }}>
                                    {analysis.clickbait.indicators.slice(0, 2).join(', ')}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Text Quality */}
                    <div className="analysis-item">
                        <div className="analysis-item-title">Text Quality</div>
                        <div className="analysis-item-value">{analysis.text_quality.score}/100</div>
                        <div className="analysis-item-description">
                            {analysis.text_quality.issues[0]}
                        </div>
                    </div>

                    {/* Sentiment Analysis */}
                    <div className="analysis-item">
                        <div className="analysis-item-title">Sentiment Analysis</div>
                        <div className="analysis-item-value">
                            {analysis.sentiment.polarity > 0 ? '😊' : analysis.sentiment.polarity < 0 ? '😟' : '😐'}
                        </div>
                        <div className="analysis-item-description">
                            Polarity: {analysis.sentiment.polarity.toFixed(2)}
                            <br />
                            Subjectivity: {analysis.sentiment.subjectivity.toFixed(2)}
                        </div>
                    </div>
                </div>

                {/* Key Findings */}
                <div className="findings-section">
                    <h3 className="findings-title">🔍 Key Findings</h3>
                    <ul className="findings-list">
                        {key_findings.map((finding, index) => (
                            <li key={index} className="finding-item">
                                {finding}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ResultsDisplay;
