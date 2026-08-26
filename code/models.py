"""
Data models for the Trust & Safety mini-pipeline.

This is an original, from-scratch implementation of the documented
Screening → Allocation decision logic — reference code, not a copy of
any production system. See README.md for the disclosure on scope.
"""

from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    DISABLED = "disabled"
    CLEAR = "clear"
    REVIEW_WITH_CAUTION = "review_with_caution"


@dataclass
class Review:
    """A single incoming review, with the signals the Screening Agent inspects."""
    review_id: str
    reviewer_id: str
    product_category: str
    content: str

    # Signals — a small illustrative set, not the real ~50-signal roster.
    ip_risk_score: int          # 0-100, simulated third-party IP risk signal
    vpn_detected: bool
    country_mismatch: bool      # submission country vs. profile-stated country
    reviewer_history_count: int  # how many prior reviews this reviewer has submitted
    is_first_time_reviewer: bool
    submissions_last_24h: int   # this reviewer's submission velocity
    duplicate_content_score: float  # 0.0-1.0, similarity to other known reviews


@dataclass
class ScreeningResult:
    review_id: str
    decision: Decision
    complexity_score: int  # 0-100
    flagged_signals: list[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class Moderator:
    """A moderator profile the Allocation Agent can route work to."""
    moderator_id: str
    name: str
    specialties: list[str]   # e.g. ["fraud", "content_quality", "identity"]
    seniority: int           # 1 (junior) to 3 (senior) — gates max complexity handled
    current_open_cases: int
    max_capacity: int


@dataclass
class AllocationResult:
    review_id: str
    assigned_moderator_id: str | None
    reason: str
