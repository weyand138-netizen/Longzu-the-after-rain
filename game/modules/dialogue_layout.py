"""Presentation-only sentence grouping; joining pages reproduces the exact copy."""
import ast
import re

MAX_PAGE_CHARACTERS = 90
DIALOGUE_PANEL_COLOR = "#0b1320"
_SAY = re.compile(r'^\s*(narrator|lm|erii|system)\s+(".*")\s*$')


def split_dialogue(text, limit=MAX_PAGE_CHARACTERS):
    if len(text) <= limit:
        return (text,)
    if limit < 20:
        raise ValueError("Dialogue page limit must allow a readable phrase")
    # Keep a sentence's closing quotation mark with its punctuation.
    sentences = re.findall(r'.+?[。！？](?:[”」』\"]+)?|.+$', text, re.DOTALL)
    units = []
    for sentence in sentences:
        while len(sentence) > limit:
            candidates = [i + 1 for i, c in enumerate(sentence[:limit]) if c in "；，：、"]
            substantial = [i for i in candidates if i >= limit // 3]
            cut = substantial[-1] if substantial else limit
            # A closing punctuation mark must not start a new page.
            while cut < len(sentence) and sentence[cut] in "”」』）】》":
                cut += 1
            units.append(sentence[:cut])
            sentence = sentence[cut:]
        if sentence:
            units.append(sentence)
    pages, current = [], ""
    for unit in units:
        if current and len(current) + len(unit) > limit:
            pages.append(current)
            current = ""
        current += unit
    if current:
        pages.append(current)
    assert "".join(pages) == text
    return tuple(pages)


def visible_copy_signature(source):
    """Ignore only adjacent display boundaries for an unchanged speaker."""
    result = []
    for line in source.splitlines():
        match = _SAY.fullmatch(line)
        if match:
            speaker, text = match[1], ast.literal_eval(match[2])
            if result and result[-1][0] == speaker:
                result[-1] = (speaker, result[-1][1] + text)
            else:
                result.append((speaker, text))
        elif re.match(r'\s*"[^"\n]+"(?:\s+if\s+.+)?:\s*$', line):
            result.append(("choice", line.strip()))
    return result
