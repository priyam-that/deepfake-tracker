"""
Content Analyzer Module
Analyzes web content for fake news detection using NLP techniques
"""

import re
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class ContentAnalyzer:
    """Analyzes content for fake news indicators"""
    
    # Known credible news sources (simplified list)
    CREDIBLE_SOURCES = {
        'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk',
        'npr.org', 'pbs.org', 'theguardian.com', 'nytimes.com',
        'washingtonpost.com', 'wsj.com', 'economist.com'
    }
    
    # Known questionable sources
    QUESTIONABLE_SOURCES = {
        'infowars.com', 'naturalnews.com', 'beforeitsnews.com'
    }
    
    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
    
    def fetch_content(self, url):
        """
        Fetch and extract text content from URL
        
        Args:
            url (str): URL to fetch content from
            
        Returns:
            dict: Contains 'title', 'text', 'domain', 'success', 'error'
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text from paragraphs
            paragraphs = soup.find_all(['p', 'article'])
            text_content = ' '.join([p.get_text().strip() for p in paragraphs])
            
            # Get domain
            domain = urlparse(url).netloc.replace('www.', '')
            
            return {
                'success': True,
                'title': title_text,
                'text': text_content,
                'domain': domain,
                'url': url
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            return {
                'success': False,
                'error': f"Failed to fetch content: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error parsing content: {e}")
            return {
                'success': False,
                'error': f"Failed to parse content: {str(e)}"
            }
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text
        
        Returns:
            dict: polarity (-1 to 1) and subjectivity (0 to 1)
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def detect_clickbait(self, title, text):
        """
        Detect clickbait indicators
        
        Returns:
            dict: clickbait score and indicators
        """
        score = 0
        indicators = []
        
        # Check for excessive punctuation
        if title.count('!') > 1:
            score += 15
            indicators.append("Excessive exclamation marks")
        
        # Check for all caps words
        words = title.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 1]
        if len(caps_words) > 2:
            score += 20
            indicators.append("Excessive capitalization")
        
        # Check for clickbait phrases
        clickbait_phrases = [
            'you won\'t believe', 'shocking', 'this one trick',
            'doctors hate', 'what happened next', 'the truth about',
            'they don\'t want you to know', 'mind-blowing'
        ]
        
        title_lower = title.lower()
        for phrase in clickbait_phrases:
            if phrase in title_lower:
                score += 25
                indicators.append(f"Clickbait phrase: '{phrase}'")
                break
        
        # Check for question in title
        if '?' in title:
            score += 5
            indicators.append("Question-based headline")
        
        # Check for numbers in title (listicles)
        if re.search(r'\b\d+\b', title):
            score += 10
            indicators.append("Number-based headline (listicle)")
        
        return {
            'score': min(score, 100),
            'indicators': indicators
        }
    
    def analyze_source_credibility(self, domain):
        """
        Analyze source credibility based on domain
        
        Returns:
            dict: credibility score and classification
        """
        if domain in self.CREDIBLE_SOURCES:
            return {
                'score': 90,
                'classification': 'Highly Credible',
                'note': 'Well-established news organization'
            }
        elif domain in self.QUESTIONABLE_SOURCES:
            return {
                'score': 20,
                'classification': 'Questionable',
                'note': 'Known for publishing misleading content'
            }
        else:
            # Default moderate score for unknown sources
            return {
                'score': 50,
                'classification': 'Unknown Source',
                'note': 'Source credibility cannot be verified'
            }
    
    def analyze_text_quality(self, text):
        """
        Analyze text quality and linguistic patterns
        
        Returns:
            dict: quality metrics
        """
        if not text or len(text) < 100:
            return {
                'score': 30,
                'issues': ['Insufficient content']
            }
        
        issues = []
        score = 100
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if caps_ratio > 0.1:
            score -= 20
            issues.append("Excessive capitalization")
        
        # Check for spelling errors (simplified)
        words = text.split()
        if len(words) > 50:
            blob = TextBlob(text[:500])  # Check first 500 chars
            # This is a simplified check
            
        # Check for very short sentences (might indicate poor quality)
        sentences = nltk.sent_tokenize(text[:1000])
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length < 5:
                score -= 15
                issues.append("Unusually short sentences")
        
        # Check for repetitive content
        words_lower = [w.lower() for w in words[:200]]
        unique_ratio = len(set(words_lower)) / len(words_lower) if words_lower else 0
        if unique_ratio < 0.3:
            score -= 20
            issues.append("Highly repetitive content")
        
        return {
            'score': max(score, 0),
            'issues': issues if issues else ['No major issues detected']
        }
    
    def calculate_credibility_score(self, analysis_data):
        """
        Calculate overall credibility score
        
        Args:
            analysis_data (dict): All analysis results
            
        Returns:
            int: Credibility score (0-100)
        """
        # Weighted scoring
        source_weight = 0.35
        clickbait_weight = 0.25
        quality_weight = 0.20
        sentiment_weight = 0.20
        
        source_score = analysis_data['source_credibility']['score']
        clickbait_penalty = analysis_data['clickbait']['score']
        quality_score = analysis_data['text_quality']['score']
        
        # Sentiment extremity (very negative or very positive can indicate bias)
        sentiment_polarity = abs(analysis_data['sentiment']['polarity'])
        sentiment_score = 100 - (sentiment_polarity * 30)
        
        # Subjectivity (higher subjectivity = less credible)
        subjectivity = analysis_data['sentiment']['subjectivity']
        sentiment_score -= (subjectivity * 20)
        
        # Calculate weighted score
        credibility = (
            source_score * source_weight +
            (100 - clickbait_penalty) * clickbait_weight +
            quality_score * quality_weight +
            max(sentiment_score, 0) * sentiment_weight
        )
        
        return int(max(min(credibility, 100), 0))
    
    def get_warning_level(self, credibility_score):
        """
        Determine warning level based on credibility score
        
        Returns:
            dict: warning level and message
        """
        if credibility_score >= 70:
            return {
                'level': 'safe',
                'label': 'Likely Credible',
                'message': 'This content appears to be from a credible source with reliable information.',
                'color': '#10b981'
            }
        elif credibility_score >= 40:
            return {
                'level': 'suspicious',
                'label': 'Verify Carefully',
                'message': 'This content shows some indicators of potential misinformation. Verify with multiple sources.',
                'color': '#f59e0b'
            }
        else:
            return {
                'level': 'dangerous',
                'label': 'High Risk',
                'message': 'This content shows multiple indicators of misinformation or fake news. Exercise extreme caution.',
                'color': '#ef4444'
            }
    
    def analyze(self, url):
        """
        Perform complete analysis on URL
        
        Args:
            url (str): URL to analyze
            
        Returns:
            dict: Complete analysis results
        """
        # Fetch content
        content_data = self.fetch_content(url)
        
        if not content_data['success']:
            return {
                'success': False,
                'error': content_data['error']
            }
        
        title = content_data['title']
        text = content_data['text']
        domain = content_data['domain']
        
        # Perform analyses
        sentiment = self.analyze_sentiment(text)
        clickbait = self.detect_clickbait(title, text)
        source_credibility = self.analyze_source_credibility(domain)
        text_quality = self.analyze_text_quality(text)
        
        # Compile analysis data
        analysis_data = {
            'sentiment': sentiment,
            'clickbait': clickbait,
            'source_credibility': source_credibility,
            'text_quality': text_quality
        }
        
        # Calculate overall credibility
        credibility_score = self.calculate_credibility_score(analysis_data)
        warning = self.get_warning_level(credibility_score)
        
        # Generate key findings
        key_findings = []
        
        if clickbait['indicators']:
            key_findings.append(f"Clickbait indicators detected: {', '.join(clickbait['indicators'][:2])}")
        
        if source_credibility['classification'] == 'Highly Credible':
            key_findings.append("Source is a well-established news organization")
        elif source_credibility['classification'] == 'Questionable':
            key_findings.append("Source has history of publishing misleading content")
        
        if sentiment['subjectivity'] > 0.6:
            key_findings.append("Content is highly subjective/opinion-based")
        
        if text_quality['issues'] and text_quality['issues'][0] != 'No major issues detected':
            key_findings.append(f"Text quality issues: {text_quality['issues'][0]}")
        
        if not key_findings:
            key_findings.append("No major red flags detected")
        
        return {
            'success': True,
            'url': url,
            'title': title,
            'domain': domain,
            'credibility_score': credibility_score,
            'warning': warning,
            'analysis': {
                'sentiment': sentiment,
                'clickbait': clickbait,
                'source_credibility': source_credibility,
                'text_quality': text_quality
            },
            'key_findings': key_findings
        }
