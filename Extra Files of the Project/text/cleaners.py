
"""Text cleaners for FastSpeech2."""

import re
import unicodedata

from unidecode import unidecode
from .numbers import normalize_numbers

# Regular expression matching whitespace
_whitespace_re = re.compile(r"\s+")

# English abbreviation replacements
_abbreviations = [
    (re.compile(r"\b%s\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("mrs", "misess"),
        ("mr", "mister"),
        ("dr", "doctor"),
        ("st", "saint"),
        ("co", "company"),
        ("jr", "junior"),
        ("maj", "major"),
        ("gen", "general"),
        ("drs", "doctors"),
        ("rev", "reverend"),
        ("lt", "lieutenant"),
        ("hon", "honorable"),
        ("sgt", "sergeant"),
        ("capt", "captain"),
        ("esq", "esquire"),
        ("ltd", "limited"),
        ("col", "colonel"),
        ("ft", "fort"),
    ]
]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
    return unidecode(text)


def basic_cleaners(text):
    """Basic pipeline: lowercase and collapse whitespace."""
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def telugu_cleaners(text):
    """Normalize Telugu Unicode text without transliteration."""
    text = unicodedata.normalize("NFC", text)
    text = collapse_whitespace(text)
    return text.strip()


def transliteration_cleaners(text):
    """Pipeline for non-English text that can be transliterated to ASCII."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def english_cleaners(text):
    """English text cleaning, including number and abbreviation expansion."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_numbers(text)
    text = expand_abbreviations(text)
    text = collapse_whitespace(text)
    return text
