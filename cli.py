#!/usr/bin/env python3
"""CLI for JD Matcher."""
import argparse
import os
import sys
from jd_matcher import analyze, jd_context


def load(path: str) -> str:
    with open(path) as f:
        return f.read()


def cmd_analyze(args):
    resume = load(args.resume)
    jd = load(args.jd)
    report = analyze(resume, jd, top_n=args.top)
    print(f"match score: {report.score:.1f}%  "
          f"({len(report.matched)}/{report.jd_keyword_count} JD keywords found)")
    if report.missing:
        print("\nmissing keywords (by JD emphasis):")
        for word, freq in report.missing[: args.show]:
            ctx = jd_context(jd, word)
            print(f"  - {word}  (x{freq})")
            if ctx:
                print(f"      e.g. \"{ctx}\"")
    else:
        print("\nno missing keywords — strong keyword coverage.")


def cmd_missing(args):
    resume = load(args.resume)
    jd = load(args.jd)
    report = analyze(resume, jd, top_n=args.top)
    for word in report.missing_words:
        print(word)


def cmd_batch(args):
    resume = load(args.resume)
    rows = []
    for name in sorted(os.listdir(args.jds)):
        if not name.endswith(".txt"):
            continue
        jd = load(os.path.join(args.jds, name))
        report = analyze(resume, jd, top_n=args.top)
        rows.append((report.score, name))
    for score, name in sorted(rows, reverse=True):
        print(f"{score:5.1f}%  {name}")


def main():
    p = argparse.ArgumentParser(prog="jd-matcher")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="full gap report for one JD")
    a.add_argument("--resume", required=True)
    a.add_argument("--jd", required=True)
    a.add_argument("--top", type=int, default=60)
    a.add_argument("--show", type=int, default=15)
    a.set_defaults(fn=cmd_analyze)

    m = sub.add_parser("missing", help="list missing keywords, one per line")
    m.add_argument("--resume", required=True)
    m.add_argument("--jd", required=True)
    m.add_argument("--top", type=int, default=60)
    m.set_defaults(fn=cmd_missing)

    b = sub.add_parser("batch", help="rank a folder of JDs by match score")
    b.add_argument("--resume", required=True)
    b.add_argument("--jds", required=True)
    b.add_argument("--top", type=int, default=60)
    b.set_defaults(fn=cmd_batch)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
