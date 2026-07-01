import re
from datetime import timedelta
from statistics import mean

from ..models import Transaction

# Tunable thresholds for treating a group of similarly-priced, similarly-named
# transactions as a recurring series. Calibrated for typical Dutch personal
# subscription pricing (small streaming/utility charges), not derived from
# any formal analysis - adjust freely based on what gets detected in practice.
AMOUNT_TOLERANCE_PCT = 0.10
AMOUNT_TOLERANCE_ABS = 1.50
MIN_GAP_DAYS = 21
MAX_GAP_DAYS = 40
MIN_OCCURRENCES = 3

IGNORED_DESCRIPTIONS = {"bank import"}


def _normalize_description(description: str) -> str:
    return re.sub(r"\s+", " ", description.strip().lower())


def _amount_matches_cluster(amount: float, cluster: list[Transaction]) -> bool:
    cluster_avg = mean(float(t.amount) for t in cluster)
    tolerance = max(AMOUNT_TOLERANCE_ABS, AMOUNT_TOLERANCE_PCT * abs(cluster_avg))

    return abs(amount - cluster_avg) <= tolerance


def _build_series(cluster: list[Transaction]) -> dict | None:
    if len(cluster) < MIN_OCCURRENCES:
        return None

    ordered = sorted(cluster, key=lambda t: t.transaction_date)
    gaps = [
        (ordered[i].transaction_date - ordered[i - 1].transaction_date).days
        for i in range(1, len(ordered))
    ]

    if not all(MIN_GAP_DAYS <= gap <= MAX_GAP_DAYS for gap in gaps):
        return None

    type_counts: dict[str, int] = {}
    for t in ordered:
        type_counts[t.type] = type_counts.get(t.type, 0) + 1
    most_common_type = max(type_counts.items(), key=lambda item: item[1])[0]

    avg_amount = mean(float(t.amount) for t in ordered)
    avg_gap_days = round(mean(gaps))

    return {
        "description": ordered[-1].description,
        "type": most_common_type,
        "avg_amount": avg_amount,
        "occurrence_count": len(ordered),
        "first_date": ordered[0].transaction_date,
        "last_date": ordered[-1].transaction_date,
        "predicted_next_date": ordered[-1].transaction_date + timedelta(days=avg_gap_days),
        "transaction_ids": [t.id for t in ordered],
        "all_marked_subscription": all(t.is_subscription for t in ordered),
    }


def detect_recurring_series(transactions: list[Transaction]) -> list[dict]:
    candidates = [
        t
        for t in transactions
        if t.transaction_date is not None
        and t.description
        and _normalize_description(t.description) not in IGNORED_DESCRIPTIONS
        and float(t.amount) < 0
    ]

    groups: dict[str, list[Transaction]] = {}
    for t in candidates:
        groups.setdefault(_normalize_description(t.description), []).append(t)

    series_list = []

    for group in groups.values():
        ordered_group = sorted(group, key=lambda t: t.transaction_date)
        clusters: list[list[Transaction]] = []

        for t in ordered_group:
            matching_cluster = next(
                (
                    cluster
                    for cluster in clusters
                    if _amount_matches_cluster(float(t.amount), cluster)
                ),
                None,
            )

            if matching_cluster is not None:
                matching_cluster.append(t)
            else:
                clusters.append([t])

        for cluster in clusters:
            series = _build_series(cluster)
            if series is not None:
                series_list.append(series)

    series_list.sort(key=lambda series: series["predicted_next_date"])

    return series_list
