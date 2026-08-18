"""Minimal statistics for engineers (ch6): intervals (single-run / multi-run clustered), significance (unpaired z / paired McNemar), flip rate, percentiles."""
import math


def interval95(passed, n):
    """95% interval for a pass rate (normal approximation). Returns (mean, half-width). For single runs; merged multi-run goes through interval95_clustered."""
    if n == 0:
        return 0.0, 0.0
    p = passed / n
    half = 1.96 * math.sqrt(p * (1 - p) / n)
    return round(p, 4), round(half, 4)


def interval95_clustered(case_means):
    """Pass-rate interval for merged multi-run: clustered by case (ch6 step 3).
    case_means: one entry per case, its k runs folded into a single pass rate. The denominator is the case count;
    treating n×k verdicts as independent samples is pseudo-replication and reports the interval about half as wide as it is. Returns (mean, half-width)."""
    n = len(case_means)
    if n == 0:
        return 0.0, 0.0
    m = sum(case_means) / n
    var = sum((x - m) ** 2 for x in case_means) / (n - 1) if n > 1 else 0.0
    half = 1.96 * math.sqrt(var / n)
    return round(m, 4), round(half, 4)


def mcnemar(a_only_pass, b_only_pass):
    """McNemar paired test (continuity-corrected, α = 0.05): two versions run the same eval set; count only the cases that flip direction.
    a_only_pass: cases A passes and B fails; b_only_pass: cases A fails and B passes.
    Cases that pass both or fail both carry no information. Returns (significant, chi2)."""
    b, c = a_only_pass, b_only_pass
    if b + c == 0:
        return False, 0.0
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    return chi2 > 3.841, round(chi2, 3)


def significant(p1, n1, p2, n2):
    """Two-proportion z test, α = 0.05. Returns (significant, z)."""
    if n1 == 0 or n2 == 0:
        return False, 0.0
    p = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se if se else 0.0
    return abs(z) > 1.96, round(z, 3)


def flip_rate(runs_by_case):
    """Flip rate: fraction of cases whose repeated runs disagree. runs_by_case: {case_id: [verdict, ...]}"""
    flips = sum(1 for vs in runs_by_case.values() if len(set(vs)) > 1)
    n = len(runs_by_case)
    return round(flips / n, 4) if n else 0.0


def percentile(values, q):
    """P50/P95 etc. q ∈ [0, 100]."""
    if not values:
        return 0.0
    xs = sorted(values)
    i = min(len(xs) - 1, max(0, math.ceil(q / 100 * len(xs)) - 1))
    return xs[i]
