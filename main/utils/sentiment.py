"""Sentiment utilities for Career Compass.

This module tries to use `vaderSentiment` if available. If not, it
falls back to a lightweight rule-based scorer so the app keeps working
without extra packages.

Functions:
  - analyze_text(text) -> {'score': float, 'label': str}
  - analyze_sentiment(text) -> same as analyze_text (compatibility)
"""
from typing import Dict

_USE_VADER = False
_VADER_ANALYZER = None
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _VADER_ANALYZER = SentimentIntensityAnalyzer()
    _USE_VADER = True
except Exception:
    _USE_VADER = False

# simple lexicons for fallback
_POS_WORDS = set(["good","great","excellent","positive","success","happy","helpful","improved","strong","love","like","recommend"]) 
_NEG_WORDS = set(["bad","poor","negative","fail","failed","sad","problem","issue","weak","hate","dislike","risk"]) 

# Emotion lexicons for detailed breakdown
_EMOTION_LEXICONS = {
    'motivated': set(['motivated', 'inspired', 'driven', 'ambitious', 'determined', 'goal', 'achieve', 'passion', 'energized']),
    'eager': set(['eager', 'excited', 'enthusiastic', 'keen', 'ready', 'anticipate', 'looking forward', 'can\'t wait']),
    'confident': set(['confident', 'sure', 'certain', 'strong', 'capable', 'skilled', 'competent', 'believe']),
    'anxious': set(['anxious', 'worried', 'nervous', 'concerned', 'stress', 'anxious', 'uneasy', 'tense']),
    'depressed': set(['depressed', 'sad', 'down', 'hopeless', 'unmotivated', 'discouraged', 'low', 'miserable']),
    'frustrated': set(['frustrated', 'annoyed', 'irritated', 'stuck', 'difficult', 'struggling', 'challenge', 'obstacle']),
    'satisfied': set(['satisfied', 'content', 'pleased', 'happy', 'fulfilled', 'accomplished', 'proud', 'good']),
}


def _fallback_score(text: str) -> float:
    if not text:
        return 0.0
    t = text.lower()
    words = [w.strip(".,!?;:\"'()[]") for w in t.split()]
    pos = sum(1 for w in words if w in _POS_WORDS)
    neg = sum(1 for w in words if w in _NEG_WORDS)
    # simple normalized score between -1 and 1
    if pos + neg == 0:
        return 0.0
    return float(pos - neg) / float(max(1, pos + neg))


def _analyze_emotions(text: str) -> Dict[str, float]:
    """Analyze text for specific emotions and return percentages."""
    if not text:
        return {emotion: 0.0 for emotion in _EMOTION_LEXICONS}
    
    text_lower = text.lower()
    words = [w.strip(".,!?;:\"'()[]") for w in text_lower.split()]
    word_set = set(words)
    
    emotion_scores = {}
    total_matches = 0
    
    for emotion, lexicon in _EMOTION_LEXICONS.items():
        matches = len(word_set.intersection(lexicon))
        emotion_scores[emotion] = matches
        total_matches += matches
    
    # Convert to percentages
    if total_matches > 0:
        emotion_percentages = {emotion: round((score / total_matches) * 100, 1) 
                              for emotion, score in emotion_scores.items()}
    else:
        # Default distribution when no emotion words found
        emotion_percentages = {emotion: 14.3 for emotion in emotion_scores}
    
    return emotion_percentages


def analyze_text(text: str) -> Dict[str, object]:
    """Return sentiment summary for `text`.

    Returns a dict with keys: 'score' (float between -1 and 1), 'label'
    (Positive/Neutral/Negative), and 'emotions' (detailed breakdown).
    """
    if not text:
        return {'score': 0.0, 'label': 'Neutral', 'emotions': _analyze_emotions('')}

    emotions = _analyze_emotions(text)
    
    try:
        if _USE_VADER and _VADER_ANALYZER is not None:
            scores = _VADER_ANALYZER.polarity_scores(text)
            c = scores.get('compound', 0.0)
            label = 'Positive' if c >= 0.05 else ('Negative' if c <= -0.05 else 'Neutral')
            return {'score': round(float(c), 3), 'label': label, 'emotions': emotions}
    except Exception:
        # fall through to fallback
        pass

    s = _fallback_score(text)
    label = 'Positive' if s > 0.05 else ('Negative' if s < -0.05 else 'Neutral')
    return {'score': round(float(s), 3), 'label': label, 'emotions': emotions}


def analyze_sentiment(text: str) -> Dict[str, object]:
    """Compatibility wrapper used by views."""
    return analyze_text(text)
