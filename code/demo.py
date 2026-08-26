"""
Demo runner — walks a batch of synthetic reviews through Screening,
then Allocation, printing each step's decision and reasoning.

Run it:
    python demo.py
"""

from __future__ import annotations

from screening_agent import screen
from allocation_agent import allocate
from sample_data import sample_reviews, sample_moderators


def divider():
    print("-" * 72)


def main():
    reviews = sample_reviews()
    moderators = sample_moderators()

    print("=" * 72)
    print("TRUST & SAFETY MINI-PIPELINE — SCREENING -> ALLOCATION")
    print(f"{len(reviews)} synthetic reviews, {len(moderators)} synthetic moderators")
    print("=" * 72)

    tally = {"disabled": 0, "clear": 0, "review_with_caution": 0}

    for review in reviews:
        divider()
        print(f"Review {review.review_id}  ({review.product_category})")
        print(f'  "{review.content[:70]}{"..." if len(review.content) > 70 else ""}"')

        result = screen(review)
        tally[result.decision.value] += 1

        print(f"  -> Screening: {result.decision.value.upper()}  (complexity {result.complexity_score}/100)")
        if result.flagged_signals:
            print(f"     signals: {', '.join(result.flagged_signals)}")
        print(f"     {result.reasoning}")

        if result.decision.value == "review_with_caution":
            alloc = allocate(review, result, moderators)
            # reflect the assignment back into the moderator's open case count
            if alloc.assigned_moderator_id:
                for m in moderators:
                    if m.moderator_id == alloc.assigned_moderator_id:
                        m.current_open_cases += 1
            print(f"  -> Allocation: {alloc.reason}")

    divider()
    print("\nSUMMARY")
    total = len(reviews)
    for key, count in tally.items():
        pct = round(100 * count / total)
        print(f"  {key:22s} {count}/{total}  ({pct}%)")


if __name__ == "__main__":
    main()
