
"""Text processing for English and Telugu FastSpeech 2."""

import re
from text import cleaners
from text.symbols import symbols
from text.telugu_symbols import symbols as telugu_symbols


# --------------------------------------------------
# ENGLISH SYMBOL MAPPINGS (UNCHANGED)
# --------------------------------------------------

_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")


def text_to_sequence(text, cleaner_names):
    """Convert English text into symbol IDs."""
    sequence = []

    while len(text):
        m = _curly_re.match(text)

        if not m:
            sequence += _symbols_to_sequence(
                _clean_text(text, cleaner_names)
            )
            break

        sequence += _symbols_to_sequence(
            _clean_text(m.group(1), cleaner_names)
        )
        sequence += _arpabet_to_sequence(m.group(2))
        text = m.group(3)

    return sequence


def sequence_to_text(sequence):
    """Convert English symbol IDs back into text."""
    result = ""

    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]

            if len(s) > 1 and s[0] == "@":
                s = "{%s}" % s[1:]

            result += s

    return result.replace("}{", " ")


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)

        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)

        text = cleaner(text)

    return text


def _symbols_to_sequence(symbols_list):
    return [
        _symbol_to_id[s]
        for s in symbols_list
        if _should_keep_symbol(s)
    ]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(
        ["@" + s for s in text.split()]
    )


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != "_" and s != "~"


# --------------------------------------------------
# TELUGU SYMBOL MAPPINGS (SEPARATE)
# --------------------------------------------------

_telugu_symbol_to_id = {
    s: i for i, s in enumerate(telugu_symbols)
}

_telugu_id_to_symbol = {
    i: s for i, s in enumerate(telugu_symbols)
}


def telugu_text_to_sequence(text):
    """Convert Telugu text into Telugu grapheme/codepoint IDs."""

    text = cleaners.telugu_cleaners(text)

    sequence = []

    for char in text:
        if char not in _telugu_symbol_to_id:
            raise ValueError(
                f"Unsupported Telugu character: {repr(char)} "
                f"(Unicode: U+{ord(char):04X})"
            )

        sequence.append(_telugu_symbol_to_id[char])

    return sequence


def telugu_sequence_to_text(sequence):
    """Convert Telugu IDs back into text."""

    result = []

    for symbol_id in sequence:
        if symbol_id not in _telugu_id_to_symbol:
            raise ValueError(
                f"Unknown Telugu symbol ID: {symbol_id}"
            )

        result.append(_telugu_id_to_symbol[symbol_id])

    return "".join(result)

