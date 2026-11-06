import unicodedata

_pad = "_"
_punctuation = "!(),.:;? "
_telugu = [chr(i) for i in range(0x0C00, 0x0C50) if unicodedata.category(chr(i))[0] in ("L", "M")]
symbols = list(dict.fromkeys([_pad] + list(_punctuation) + _telugu))
