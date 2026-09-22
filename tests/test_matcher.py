from jd_matcher import analyze, keywords, tokenize


def test_keywords_rank_by_frequency():
    kw = dict(keywords("python python python kubernetes", top_n=10))
    assert kw["python"] == 3
    assert "kubernetes" in kw


def test_stopwords_dropped():
    assert "the" not in tokenize("the quick brown fox")


def test_analyze_finds_gap():
    resume = "Python developer with Postgres and Docker experience."
    jd = "We need Kubernetes and Terraform experience. Kubernetes in production."
    report = analyze(resume, jd, top_n=20)
    assert "kubernetes" in report.missing_words
    assert report.score < 100


def test_perfect_match_scores_100():
    text = "Python Kubernetes Terraform"
    report = analyze(text, text, top_n=10)
    assert report.score == 100.0
    assert report.missing == []
