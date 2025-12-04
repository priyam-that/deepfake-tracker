"""
Deepfake AI Tracker - Flask Backend
Main application file for fake news detection API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import ContentAnalyzer
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Allow requests from frontend
allowed_origins = [
    "http://localhost:5173",  # Local development
    "http://localhost:3000",  # Alternative local port 
    "https://deepfaketracker.netlify.app",  # Netlify deployment
    "https://deploy-preview-*.netlify.app",  # Netlify preview deployments
]

# Get additional allowed origins from environment variable if set
env_origins = os.environ.get('ALLOWED_ORIGINS', '')
if env_origins:
    allowed_origins.extend(env_origins.split(','))

CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize analyzer
analyzer = ContentAnalyzer()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Deepfake AI Tracker API is running'
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """
    Analyze URL for fake news detection
    
    Expected JSON body:
    {
        "url": "https://example.com/article"
    }
    
    Returns:
    {
        "success": true,
        "credibility_score": 75,
        "warning": {...},
        "analysis": {...},
        "key_findings": [...]
    }
    """
    try:
        # Get URL from request
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        url = data['url'].strip()
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }), 400
        
        logger.info(f"Analyzing URL: {url}")
        
        # Perform analysis
        result = analyzer.analyze(url)
        
        if not result['success']:
            return jsonify(result), 400
        
        logger.info(f"Analysis complete. Credibility score: {result['credibility_score']}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_url: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple URLs
    
    Expected JSON body:
    {
        "urls": ["url1", "url2", ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'success': False,
                'error': 'URLs array is required'
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({
                'success': False,
                'error': 'URLs must be a non-empty array'
            }), 400
        
        if len(urls) > 10:
            return jsonify({
                'success': False,
                'error': 'Maximum 10 URLs allowed per batch'
            }), 400
        
        results = []
        for url in urls:
            result = analyzer.analyze(url.strip())
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch_analyze: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


if __name__ == '__main__':
    logger.info("Starting Deepfake AI Tracker API...")
    logger.info("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
