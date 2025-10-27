import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
import logging

# Download NLTK resources if not present
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)

class AdvancedExtractor:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        self.cluster_model = None

    def analyze_psychology(self, text):
        """
        Analyze text for psychological elements using first principles of criminal/business psychology,
        Bloom's taxonomy, neurolinguistic programming, and predictive analytics.
        """
        analysis = {
            'sentiment': self.sia.polarity_scores(text),
            'motive_indicators': self._extract_motive_indicators(text),
            'communication_style': self._analyze_communication_style(text),
            'predictive_indicators': self._extract_predictive_indicators(text),
            'blooms_level': self._assess_blooms_taxonomy(text),
            'nlp_patterns': self._detect_nlp_patterns(text)
        }
        return analysis

    def categorize_evidence(self, text):
        """
        Categorize evidence using investigative principles and lawyer communication skills.
        """
        categories = {
            'direct_evidence': self._detect_direct_evidence(text),
            'circumstantial_evidence': self._detect_circumstantial_evidence(text),
            'hearsay': self._detect_hearsay(text),
            'documentary_evidence': self._detect_documentary_evidence(text),
            'testimonial_evidence': self._detect_testimonial_evidence(text)
        }
        return categories

    def strategic_reasoning(self, text, context=None):
        """
        Apply strategic reasoning for relationships, motives, and context understanding.
        """
        reasoning = {
            'relationships': self._infer_relationships(text),
            'motives': self._infer_motives(text),
            'context': self._analyze_context(text, context),
            'risk_assessment': self._assess_risk(text)
        }
        return reasoning

    def _extract_motive_indicators(self, text):
        """
        Extract indicators of motives based on psychological principles.
        """
        motive_patterns = {
            'financial_gain': r'\b(money|profit|financial|wealth|rich)\b',
            'power_control': r'\b(power|control|authority|dominance|influence)\b',
            'revenge': r'\b(revenge|retaliation|payback|settle.*score)\b',
            'ideological': r'\b(belief|ideology|principle|cause|mission)\b',
            'emotional': r'\b(anger|hate|love|jealousy|greed)\b'
        }
        indicators = {}
        for motive, pattern in motive_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators[motive] = len(matches)
        return indicators

    def _analyze_communication_style(self, text):
        """
        Analyze communication style using NLP principles.
        """
        style = {
            'assertive': len(re.findall(r'\b(I|we|our)\b', text)),
            'passive': len(re.findall(r'\b(maybe|perhaps|possibly)\b', text)),
            'aggressive': len(re.findall(r'\b(always|never|must|should)\b', text)),
            'manipulative': len(re.findall(r'\b(you.*should|you.*must|you.*have.*to)\b', text))
        }
        dominant_style = max(style, key=style.get)
        return {'styles': style, 'dominant': dominant_style}

    def _extract_predictive_indicators(self, text):
        """
        Extract indicators for predictive analytics in legal contexts.
        """
        indicators = {
            'risk_words': len(re.findall(r'\b(risk|danger|threat|warning|caution)\b', text)),
            'temporal_markers': len(re.findall(r'\b(before|after|during|since|until)\b', text)),
            'conditional_language': len(re.findall(r'\b(if|then|when|unless|provided)\b', text)),
            'quantitative_terms': len(re.findall(r'\b(\d+|percent|rate|increase|decrease)\b', text))
        }
        return indicators

    def _assess_blooms_taxonomy(self, text):
        """
        Assess Bloom's taxonomy level in the text.
        """
        levels = {
            'remember': r'\b(what|who|when|where|define|list|recall)\b',
            'understand': r'\b(explain|describe|summarize|interpret|compare)\b',
            'apply': r'\b(use|apply|demonstrate|solve|implement)\b',
            'analyze': r'\b(analyze|compare|contrast|examine|investigate)\b',
            'evaluate': r'\b(evaluate|judge|critique|assess|recommend)\b',
            'create': r'\b(create|design|develop|construct|propose)\b'
        }
        scores = {}
        for level, pattern in levels.items():
            scores[level] = len(re.findall(pattern, text, re.IGNORECASE))
        return max(scores, key=scores.get) if any(scores.values()) else 'remember'

    def _detect_nlp_patterns(self, text):
        """
        Detect neurolinguistic programming patterns.
        """
        patterns = {
            'visual': r'\b(see|look|view|appear|picture|image)\b',
            'auditory': r'\b(hear|listen|sound|voice|tone|rhythm)\b',
            'kinesthetic': r'\b(feel|touch|sense|emotion|intuition)\b',
            'meta_model': r'\b(all|never|every|none|always)\b'
        }
        detected = {}
        for pattern_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected[pattern_type] = matches[:5]  # Limit to first 5 examples
        return detected

    def _detect_direct_evidence(self, text):
        return bool(re.search(r'\b(I\s+saw|I\s+heard|I\s+witnessed|eyewitness|firsthand)\b', text, re.IGNORECASE))

    def _detect_circumstantial_evidence(self, text):
        return bool(re.search(r'\b(indicates|suggests|implies|circumstantial|inference)\b', text, re.IGNORECASE))

    def _detect_hearsay(self, text):
        return bool(re.search(r'\b(said|told|according\s+to|reportedly|allegedly)\b', text, re.IGNORECASE))

    def _detect_documentary_evidence(self, text):
        return bool(re.search(r'\b(document|contract|agreement|letter|email|record)\b', text, re.IGNORECASE))

    def _detect_testimonial_evidence(self, text):
        return bool(re.search(r'\b(testimony|statement|deposition|affidavit|sworn)\b', text, re.IGNORECASE))

    def _infer_relationships(self, text):
        relationships = []
        # Simple relationship inference based on co-occurrence
        parties = re.findall(r'Party\s+[A-Z]', text)
        if len(parties) > 1:
            for i in range(len(parties)):
                for j in range(i+1, len(parties)):
                    relationships.append({
                        'party1': parties[i],
                        'party2': parties[j],
                        'type': 'ASSOCIATED_WITH'
                    })
        return relationships

    def _infer_motives(self, text):
        motives = []
        if 'financial' in self._extract_motive_indicators(text):
            motives.append('Financial Gain')
        if 'power' in self._extract_motive_indicators(text):
            motives.append('Power/Control')
        return motives

    def _analyze_context(self, text, context=None):
        context_analysis = {
            'urgency': bool(re.search(r'\b(urgent|immediate|asap|deadline)\b', text, re.IGNORECASE)),
            'confidentiality': bool(re.search(r'\b(confidential|private|secret|do\s+not\s+disclose)\b', text, re.IGNORECASE)),
            'emotional_tone': 'positive' if self.sia.polarity_scores(text)['compound'] > 0.1 else 'negative' if self.sia.polarity_scores(text)['compound'] < -0.1 else 'neutral'
        }
        if context:
            context_analysis['external_context'] = context
        return context_analysis

    def _assess_risk(self, text):
        risk_score = 0
        risk_words = ['risk', 'danger', 'threat', 'liability', 'penalty', 'fine', 'lawsuit']
        for word in risk_words:
            risk_score += len(re.findall(r'\b' + word + r'\b', text, re.IGNORECASE))
        return {'score': min(risk_score, 10), 'level': 'high' if risk_score > 5 else 'medium' if risk_score > 2 else 'low'}

def analyze_psychology(text):
    extractor = AdvancedExtractor()
    return extractor.analyze_psychology(text)

def categorize_evidence(text):
    extractor = AdvancedExtractor()
    return extractor.categorize_evidence(text)

def strategic_reasoning(text, context=None):
    extractor = AdvancedExtractor()
    return extractor.strategic_reasoning(text, context)
