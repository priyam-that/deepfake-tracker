# Deepfake AI Tracker

AI-powered fake news and deepfake detection tool that analyzes URLs to identify misinformation, clickbait, and questionable content.

## 🚀 Features

- **URL Analysis**: Analyze any news article or web content by URL
- **Credibility Scoring**: Get a 0-100 credibility score based on multiple factors
- **Warning Levels**: Visual indicators (Safe/Suspicious/Dangerous)
- **Detailed Analysis**:
  - Source credibility assessment
  - Clickbait detection
  - Text quality analysis
  - Sentiment analysis
- **Modern UI**: Dark mode with glassmorphism effects and smooth animations
- **Real-time Results**: Instant analysis with visual feedback

## 🛠️ Technology Stack

### Backend
- **Python 3.x**
- **Flask**: REST API framework
- **BeautifulSoup4**: Web scraping
- **NLTK**: Natural language processing
- **TextBlob**: Sentiment analysis

### Frontend
- **React 18**
- **Vite**: Build tool
- **Modern CSS**: Custom design system with animations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🎯 Usage

1. **Start both servers** (backend on port 5000, frontend on port 5173)

2. **Open your browser** and navigate to `http://localhost:5173`

3. **Enter a URL** of any news article or web content

4. **Click "Analyze URL"** to get instant results including:
   - Overall credibility score
   - Warning level
   - Source credibility
   - Clickbait detection
   - Text quality metrics
   - Sentiment analysis
   - Key findings

## 🔌 API Documentation

### Endpoints

#### `POST /api/analyze`
Analyze a single URL for fake news detection.

**Request Body:**
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com/article",
  "title": "Article Title",
  "domain": "example.com",
  "credibility_score": 75,
  "warning": {
    "level": "safe",
    "label": "Likely Credible",
    "message": "This content appears to be from a credible source...",
    "color": "#10b981"
  },
  "analysis": {
    "sentiment": {...},
    "clickbait": {...},
    "source_credibility": {...},
    "text_quality": {...}
  },
  "key_findings": [...]
}
```

#### `GET /api/health`
Health check endpoint.

#### `POST /api/batch-analyze`
Analyze multiple URLs (max 10 per request).

**Request Body:**
```json
{
  "urls": ["url1", "url2", "url3"]
}
```

## 🧪 How It Works

The analysis uses multiple NLP techniques:

1. **Source Credibility**: Checks domain against known credible/questionable sources
2. **Clickbait Detection**: Analyzes headlines for sensationalism indicators
3. **Text Quality**: Evaluates writing quality and linguistic patterns
4. **Sentiment Analysis**: Measures emotional tone and subjectivity
5. **Weighted Scoring**: Combines all factors into a final credibility score

## ⚠️ Limitations

- Text-based analysis only (no image/video deepfake detection yet)
- Some websites may block scraping
- Accuracy depends on content availability
- Not a replacement for professional fact-checking

## 🔮 Future Enhancements

- Image and video deepfake detection
- Integration with fact-checking APIs
- Browser extension
- Historical analysis tracking
- More advanced ML models (BERT, GPT-based)

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
