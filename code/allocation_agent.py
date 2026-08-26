"""
Allocation Agent — Layer 2, Allocation.

Takes reviews that Screening flagged as review-with-caution and routes
each one to the best-suited available moderator, based on specialty
match, seniority vs. complexity, and current load.

This replaces what the documented system describes as a 2-2.5 hour
manual daily triage process — a person going through the queue by hand
and assigning cases based on memory of who's good at what and who has
room on their plate.
"""

from models import Review, ScreeningResult, Moderator, AllocationResult


def _specialty_match_score(review_flags: list[str], moderator: Moderator) -> int:
    """How well does this moderator's specialty list match the review's flagged signals?"""
    signal_to_specialty = {
        "high_ip_risk": "fraud",
        "vpn_detected": "fraud",
        "country_mismatch": "fraud",
        "duplicate_content": "content_quality",
        "high_velocity": "fraud",
        "first_time_reviewer": "identity",
    }
    relevant_specialties = {signal_to_specialty[f] for f in review_flags if f in signal_to_specialty}
    return len(relevant_specialties & set(moderator.specialties))


def allocate(
    review: Review,
    screening: ScreeningResult,
    moderators: list[Moderator],
) -> AllocationResult:
    if screening.decision.value != "review_with_caution":
        return AllocationResult(
            review_id=review.review_id,
            assigned_moderator_id=None,
            reason="Not routed to a moderator — resolved automatically by Screening.",
        )

    # Only consider moderators with spare capacity.
    available = [m for m in moderators if m.current_open_cases < m.max_capacity]
    if not available:
        return AllocationResult(
            review_id=review.review_id,
            assigned_moderator_id=None,
            reason="No moderator capacity available — queued.",
        )

    # Complexity gates seniority: high-complexity cases need a senior moderator.
    required_seniority = 3 if screening.complexity_score >= 85 else (2 if screening.complexity_score >= 65 else 1)
    eligible = [m for m in available if m.seniority >= required_seniority] or available

    # Rank by specialty match first, then by whoever has the most spare capacity.
    ranked = sorted(
        eligible,
        key=lambda m: (
            -_specialty_match_score(screening.flagged_signals, m),
            m.current_open_cases - m.max_capacity,  # more negative = more room
        ),
    )
    chosen = ranked[0]
    match_score = _specialty_match_score(screening.flagged_signals, chosen)

    return AllocationResult(
        review_id=review.review_id,
        assigned_moderator_id=chosen.moderator_id,
        reason=(
            f"Routed to {chosen.name} — specialty match score {match_score}, "
            f"seniority {chosen.seniority}, {chosen.current_open_cases}/{chosen.max_capacity} cases open."
        ),
    )
