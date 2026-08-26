"""
Synthetic sample data — entirely made up for this demo. No real reviewer
data, no real moderator names, no real production signal values.
"""

from models import Review, Moderator


def sample_reviews() -> list[Review]:
    return [
        Review(
            review_id="R-1001", reviewer_id="U-501", product_category="CRM Software",
            content="Great tool, our team switched over easily and support has been responsive.",
            ip_risk_score=12, vpn_detected=False, country_mismatch=False,
            reviewer_history_count=14, is_first_time_reviewer=False,
            submissions_last_24h=1, duplicate_content_score=0.05,
        ),
        Review(
            review_id="R-1002", reviewer_id="U-988", product_category="Project Management",
            content="Amazing product 10/10 best tool ever amazing",
            ip_risk_score=81, vpn_detected=True, country_mismatch=True,
            reviewer_history_count=0, is_first_time_reviewer=True,
            submissions_last_24h=7, duplicate_content_score=0.94,
        ),
        Review(
            review_id="R-1003", reviewer_id="U-702", product_category="HR Software",
            content="Good onboarding experience, though the reporting module needs work.",
            ip_risk_score=55, vpn_detected=True, country_mismatch=True,
            reviewer_history_count=2, is_first_time_reviewer=False,
            submissions_last_24h=1, duplicate_content_score=0.10,
        ),
        Review(
            review_id="R-1004", reviewer_id="U-119", product_category="Marketing Automation",
            content="Solid platform, integrates well with our existing stack.",
            ip_risk_score=8, vpn_detected=False, country_mismatch=False,
            reviewer_history_count=31, is_first_time_reviewer=False,
            submissions_last_24h=1, duplicate_content_score=0.02,
        ),
        Review(
            review_id="R-1005", reviewer_id="U-844", product_category="CRM Software",
            content="Excellent value, would recommend to any small business.",
            ip_risk_score=76, vpn_detected=True, country_mismatch=False,
            reviewer_history_count=0, is_first_time_reviewer=True,
            submissions_last_24h=4, duplicate_content_score=0.15,
        ),
        Review(
            review_id="R-1006", reviewer_id="U-333", product_category="Accounting Software",
            content="Works fine for basic invoicing, wish it had better reporting.",
            ip_risk_score=22, vpn_detected=False, country_mismatch=False,
            reviewer_history_count=5, is_first_time_reviewer=False,
            submissions_last_24h=1, duplicate_content_score=0.08,
        ),
    ]


def sample_moderators() -> list[Moderator]:
    return [
        Moderator(moderator_id="M-01", name="Aisha Khan", specialties=["fraud"], seniority=3,
                   current_open_cases=3, max_capacity=6),
        Moderator(moderator_id="M-02", name="Raj Verma", specialties=["content_quality", "identity"], seniority=2,
                   current_open_cases=4, max_capacity=5),
        Moderator(moderator_id="M-03", name="Lena Ortiz", specialties=["fraud", "identity"], seniority=1,
                   current_open_cases=1, max_capacity=4),
    ]
