"""
Screening Agent — Layer 1, Proactive.

Takes an incoming review, evaluates it against a set of signals, and
returns a disable / clear / review-with-caution decision plus a 0-100
complexity score.

Design notes (matching the documented behaviour of the real system,
reimplemented from scratch with original thresholds and weights):

- A small set of hard-fail signal COMBINATIONS can disable a review
  outright, regardless of the numeric complexity score.
- Otherwise, a weighted complexity score is computed from the signals.
- The clear vs. review-with-caution split depends on the score AND on
  whether specific high-risk signal combinations are present — not on
  the score in isolation. This mirrors the real system's documented
  design: two reviews with the same score can get different outcomes
  depending on which specific signals produced that score.
"""

from __future__ import annotations

from models import Review, ScreeningResult, Decision


# Hard-fail rules: if ALL conditions in a rule are met, disable outright,
# no matter what the computed complexity score would have been.
def _hard_fail_checks(review: Review) -> str | None:
    if review.duplicate_content_score > 0.9 and review.is_first_time_reviewer:
        return "near-duplicate content from a first-time reviewer"
    if review.vpn_detected and review.country_mismatch and review.submissions_last_24h > 5:
        return "VPN + country mismatch + high submission velocity"
    return None


def _compute_complexity_score(review: Review) -> tuple[int, list[str]]:
    """Weighted scoring — original formula, not the real system's weights."""
    score = 0
    flags: list[str] = []

    if review.ip_risk_score >= 70:
        score += 30
        flags.append("high_ip_risk")
    elif review.ip_risk_score >= 40:
        score += 15

    if review.vpn_detected:
        score += 15
        flags.append("vpn_detected")

    if review.country_mismatch:
        score += 15
        flags.append("country_mismatch")

    if review.submissions_last_24h > 3:
        score += 15
        flags.append("high_velocity")

    if review.duplicate_content_score > 0.6:
        score += 20
        flags.append("duplicate_content")

    if review.is_first_time_reviewer:
        score += 10
        flags.append("first_time_reviewer")

    # Established reviewers earn trust back — score reduction, floored at 0.
    trust_discount = min(review.reviewer_history_count, 20)
    score = max(0, score - trust_discount)

    return min(score, 100), flags


# Signal combinations that force a "review with caution" outcome even
# when the raw score alone wouldn't have crossed the threshold.
_ESCALATING_COMBINATIONS = [
    {"vpn_detected", "country_mismatch"},
    {"high_ip_risk", "high_velocity"},
]


def screen(review: Review) -> ScreeningResult:
    hard_fail_reason = _hard_fail_checks(review)
    if hard_fail_reason:
        return ScreeningResult(
            review_id=review.review_id,
            decision=Decision.DISABLED,
            complexity_score=100,
            flagged_signals=["hard_fail"],
            reasoning=f"Disabled outright: {hard_fail_reason}",
        )

    score, flags = _compute_complexity_score(review)
    flag_set = set(flags)

    escalated = any(combo.issubset(flag_set) for combo in _ESCALATING_COMBINATIONS)

    if score >= 65 or escalated:
        decision = Decision.REVIEW_WITH_CAUTION
        reasoning = (
            f"Complexity score {score}/100"
            + (" with an escalating signal combination" if escalated else "")
            + " — routed to a human moderator."
        )
    else:
        decision = Decision.CLEAR
        reasoning = f"Complexity score {score}/100, no escalating signal combination — auto-cleared."

    return ScreeningResult(
        review_id=review.review_id,
        decision=decision,
        complexity_score=score,
        flagged_signals=flags,
        reasoning=reasoning,
    )
