# JD Matcher

Paste in a job description, point it at your resume text, and get an honest
keyword gap analysis: match score, the keywords you're missing, and where
they appear in the JD — so you can tailor each application in minutes.

No dependencies, no API keys, everything runs locally.

## Quick start

```bash
# analyse a resume against a job description
python cli.py analyze --resume example_resume.txt --jd example_jd.txt

# just the missing keywords, one per line (great for piping)
python cli.py missing --resume example_resume.txt --jd example_jd.txt

# compare against several JDs at once
python cli.py batch --resume example_resume.txt --jds jds/
```

## How the score works

1. Both documents are tokenised into unigrams + bigrams, minus stopwords.
2. Keywords are ranked by frequency in the JD (what the JD emphasises most).
3. Score = frequency-weighted share of JD keywords also present in the resume.

The score is a tailoring guide, not a verdict — a low score on a great-fit
role usually means the resume just doesn't *say* the right words yet.

## Files

- `jd_matcher.py` — the analyser (import it in your own tooling)
- `cli.py` — command-line interface
