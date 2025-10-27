import pytest
from kg.advanced_extraction import AdvancedExtractor

def test_analyze_psychology():
    extractor = AdvancedExtractor()
    text = "The defendant showed clear signs of financial desperation, which may indicate motive for fraud."
    result = extractor.analyze_psychology(text)

    assert "motive_indicators" in result
    assert isinstance(result["motive_indicators"], dict)
    assert len(result["motive_indicators"]) > 0

def test_categorize_evidence():
    extractor = AdvancedExtractor()
    text = "Contract signed on 2023-01-15 shows clear breach of terms regarding payment deadlines."
    result = extractor.categorize_evidence(text)

    assert "documentary_evidence" in result
    assert result["documentary_evidence"] is True

def test_strategic_reasoning():
    extractor = AdvancedExtractor()
    text = "Party A consistently uses delaying tactics in negotiations, suggesting strategic positioning for leverage."
    result = extractor.strategic_reasoning(text)

    assert "context" in result
    assert isinstance(result["context"], dict)
    assert "risk_assessment" in result

def test_communication_style_analysis():
    extractor = AdvancedExtractor()
    text = "The email was aggressive and demanding, using capital letters and exclamation points."
    result = extractor.analyze_psychology(text)

    assert "communication_style" in result
    assert isinstance(result["communication_style"], dict)
    assert "dominant" in result["communication_style"]

def test_predictive_indicators():
    extractor = AdvancedExtractor()
    text = "Multiple late payments and sudden asset transfers suggest potential insolvency proceedings."
    result = extractor.strategic_reasoning(text)

    assert "risk_assessment" in result
    assert isinstance(result["risk_assessment"], dict)
    assert "level" in result["risk_assessment"]
