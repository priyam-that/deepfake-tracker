import { useState } from 'react';
import './index.css';
import Header from './components/Header';
import AnalysisForm from './components/AnalysisForm';
import ResultsDisplay from './components/ResultsDisplay';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const analyzeUrl = async (url) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze URL');
      }

      if (data.success) {
        setResults(data);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to the server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <Header />

        <AnalysisForm onAnalyze={analyzeUrl} loading={loading} />

        {error && (
          <div className="error-message mt-lg">
            ⚠️ {error}
          </div>
        )}

        {results && <ResultsDisplay results={results} />}
      </div>
    </div>
  );
}

export default App;
