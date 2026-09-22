"""Resume vs job-description keyword gap analysis. Stdlib only."""
from __future__ import annotations
import re
from collections import Counter
from dataclasses import dataclass, field

STOPWORDS = frozenset("""
a an and are as at be been by for from has have in is it its of on or that the
to was were will with you your we our they their this these those then than
all any can could should would may might must shall do does did done not no
so such very about into over after before between through during under again
further once here there when where why how what which who whom whose
per via etc including include includes included within without across plus
join join us team work working closely help helps ability strong proven
excellent good great passionate self driven detail oriented fast paced
""".split())

TOKEN_RE = re.compile(r"[a-z][a-z0-9+#.\-]*[a-z0-9+#]|[a-z]")


def tokenize(text: str) -> list[str]:
    toks = [t.strip(".-") for t in TOKEN_RE.findall(text.lower())]
    return [t for t in toks if len(t) > 2 and t not in STOPWORDS]


def keywords(text: str, top_n: int = 60) -> list[tuple[str, int]]:
    """Top unigram + bigram keywords by frequency."""
    toks = tokenize(text)
    counts: Counter = Counter(toks)
    bigrams = [" ".join(p) for p in zip(toks, toks[1:])]
    counts.update(bigrams)
    # drop bigrams whose parts are both rare noise; keep it simple: rank all
    return counts.most_common(top_n)


@dataclass
class MatchReport:
    score: float
    matched: list[tuple[str, int]] = field(default_factory=list)
    missing: list[tuple[str, int]] = field(default_factory=list)
    jd_keyword_count: int = 0

    @property
    def matched_words(self) -> list[str]:
        return [w for w, _ in self.matched]

    @property
    def missing_words(self) -> list[str]:
        return [w for w, _ in self.missing]


def analyze(resume_text: str, jd_text: str, top_n: int = 60) -> MatchReport:
    jd_kw = keywords(jd_text, top_n)
    resume_vocab = set(tokenize(resume_text))
    # also add resume bigrams to vocab
    rtoks = tokenize(resume_text)
    resume_vocab.update(" ".join(p) for p in zip(rtoks, rtoks[1:]))

    matched, missing = [], []
    num = den = 0
    for word, freq in jd_kw:
        den += freq
        if word in resume_vocab:
            matched.append((word, freq))
            num += freq
        else:
            missing.append((word, freq))
    score = (num / den * 100) if den else 0.0
    return MatchReport(score=score, matched=matched, missing=missing,
                       jd_keyword_count=len(jd_kw))


def jd_context(jd_text: str, keyword: str, width: int = 90) -> str:
    """First JD line containing the keyword, trimmed for display."""
    for line in jd_text.splitlines():
        if keyword in line.lower():
            line = " ".join(line.split())
            return line[:width] + ("…" if len(line) > width else "")
    return ""
