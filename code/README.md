# Code — Screening & Allocation Mini-Pipeline

> **Scope note:** This is an original, from-scratch implementation of the *documented decision logic* — the screening rules, the complexity scoring approach, the allocation routing — reimplemented independently with my own thresholds and weights, running on synthetic data. It is not, and does not attempt to be, a copy of the actual production system, which belongs to my former employer and isn't mine to publish. See the main [README](../README.md) for the full system documentation.

## What's here

- `models.py` — data classes for reviews, moderators, and decision results
- `screening_agent.py` — the disable / clear / review-with-caution logic
- `allocation_agent.py` — routes flagged reviews to the best-suited available moderator
- `sample_data.py` — six synthetic reviews and three synthetic moderator profiles, made up for this demo
- `demo.py` — runs the sample data through both agents and prints each decision

## Run it

```bash
python demo.py
```

No dependencies beyond the Python standard library — Python 3.10+ (uses `list[str]` and `X | None` type hints).

## What the logic actually does

**Screening** checks each review against a handful of signals — IP risk, VPN use, a country mismatch between where the review was submitted and where the reviewer says they're based, submission velocity, content duplication, and reviewer history. A couple of signal *combinations* (not single signals) trigger an outright disable. Everything else gets a 0–100 complexity score, and — matching the real system's documented behaviour — two reviews with the same score can land differently depending on which specific signals produced it, not the score in isolation.

**Allocation** only sees the reviews that Screening couldn't resolve on its own. It matches each one to a moderator by specialty relevance, checks that moderator's seniority against the review's complexity, and picks whoever has both the right skill match and available capacity.

## A sample run

```
Review R-1003  (HR Software)
  -> Screening: REVIEW_WITH_CAUTION  (complexity 43/100)
     signals: vpn_detected, country_mismatch
  -> Allocation: Routed to Aisha Khan — specialty match score 1, seniority 3, 3/6 cases open.
```
