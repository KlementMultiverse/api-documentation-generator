import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer import LogParser, LogEntry, PatternDetector, AIAnalyzer


def test_log_parser_basic():
    """Test basic log parsing"""
    parser = LogParser()
    entry = parser._parse_line("2024-01-15 14:23:15 ERROR: Test error message")

    assert entry is not None
    assert entry.level == "ERROR"
    assert "Test error message" in entry.message


def test_log_parser_different_formats():
    """Test parsing different log formats"""
    parser = LogParser()

    # ISO format
    entry1 = parser._parse_line("2024-01-15 14:23:15 ERROR: Message1")
    assert entry1.level == "ERROR"

    # Bracket format
    entry2 = parser._parse_line("[ERROR] Message2")
    assert entry2.level == "ERROR"

    # Generic
    entry3 = parser._parse_line("ERROR: Message3")
    assert entry3.level == "ERROR"


def test_pattern_detector():
    """Test pattern detection"""
    detector = PatternDetector()

    entries = [
        LogEntry("14:00:00", "INFO", "Normal message", "raw"),
        LogEntry("14:00:01", "ERROR", "Connection failed", "raw"),
        LogEntry("14:00:02", "ERROR", "Connection failed", "raw"),
        LogEntry("14:00:03", "ERROR", "Timeout", "raw"),
    ]

    patterns = detector.analyze(entries)

    assert patterns['total_entries'] == 4
    assert patterns['error_count'] == 3
    assert 'ERROR' in patterns['level_counts']


def test_ai_analyzer_fallback():
    """Test AI analyzer fallback mode"""
    analyzer = AIAnalyzer(api_key=None)  # No API key = fallback mode

    patterns = {
        'total_entries': 10,
        'error_count': 5,
        'unique_errors': 3,
        'top_errors': [("Connection refused to database", 3)]
    }

    errors = [
        LogEntry("14:00:00", "ERROR", "Connection refused to database", "raw")
    ]

    analysis = analyzer.analyze(patterns, errors)

    assert "ROOT CAUSE" in analysis
    assert "FIXES" in analysis
    assert "PREVENTION" in analysis


def test_log_entry_creation():
    """Test LogEntry creation"""
    entry = LogEntry(
        timestamp="2024-01-15 14:23:15",
        level="ERROR",
        message="Test message",
        raw="Raw log line"
    )

    assert entry.timestamp == "2024-01-15 14:23:15"
    assert entry.level == "ERROR"
    assert entry.message == "Test message"


def test_pattern_normalization():
    """Test message normalization"""
    detector = PatternDetector()

    msg1 = detector._normalize_message("Connection to server 123 failed")
    msg2 = detector._normalize_message("Connection to server 456 failed")

    # Numbers should be normalized to 'N'
    assert msg1 == msg2
