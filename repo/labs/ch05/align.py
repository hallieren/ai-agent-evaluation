"""Chapter 5 alignment tool (offline): judge verdicts vs human labels → disagreement rate layered by severity.

Usage: python labs/ch05/align.py <judge-verdicts.jsonl> [<human-labels.jsonl>]
  human-labels defaults to labs/ch05/human-labels-sample.jsonl (a format sample; replace it with your blind labels).
Both files are verdict-record JSONL (contract section 5 schema); records align by case_id, and the layering key is the human record's severity.
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import judge, trace  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main(judge_path, human_path):
    judge_records = trace.load(judge_path)
    human_records = trace.load(human_path)
    layers = judge.align(judge_records, human_records)
    if not layers:
        sys.exit("Zero matches: the two files share no case_id; check the inputs.")
    matched = sum(d["n"] for d in layers.values())
    print(f"{len(judge_records)} judge verdicts × {len(human_records)} human labels, "
          f"{matched} matched by case_id\n")
    print(judge.render_align(layers, judge.align_recall(judge_records, human_records)))
    print("\nRead the disagreements: read each case and look for the patterns where the judge deceives you. "
          "Check first for long, polite unauthorized commitments (judge-tone-commitment's soft spot) "
          "and reports whose citations are complete but twist their sources (judge-report-rubric's soft spot).")


if __name__ == "__main__":
    assert len(sys.argv) >= 2, __doc__
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2
         else os.path.join(HERE, "human-labels-sample.jsonl"))
