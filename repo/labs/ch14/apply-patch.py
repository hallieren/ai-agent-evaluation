"""ch14 Lab step 2: apply/revert the "harmless" prompt patch (patch-sample.txt) and run the gate.

The variant seam is identical to labs/ch06: the variant file holds only the **appended line**, and before a run
`agent.SYSTEM = factory SYSTEM + "\\n" + appended line` (Mini itself does not read the prompt file, the consumption
is in the lab orchestration layer; ch6's prompt-b.txt is this very line, that time it lost to variant A, this time
it dies before merge).

Usage:
  python labs/ch14/apply-patch.py apply    # write the patch line into prompt-variant.txt
  python labs/ch14/apply-patch.py revert   # revert (variant back to the factory baseline)
  python labs/ch14/apply-patch.py status   # show the current variant
  python labs/ch14/apply-patch.py gate     # run ci/gate with the current variant (a red light exits non-zero)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from mini import agent  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANT = os.path.join(HERE, "prompt-variant.txt")


def read(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    assert cmd in ("apply", "revert", "status", "gate"), __doc__
    patch = read(os.path.join(HERE, "patch-sample.txt"))
    extra = read(VARIANT)
    if cmd == "apply":
        if extra == patch:
            print("Patch already in the variant, no need to reapply.")
        else:
            with open(VARIANT, "w", encoding="utf-8") as f:
                f.write(patch + "\n")
            print(f"[apply] prompt-variant.txt <- {patch!r}\n"
                  "Next: python labs/ch14/apply-patch.py gate, watch it die before merge.")
    elif cmd == "revert":
        if not extra:
            print("No appended line in the variant, already the factory baseline.")
        else:
            with open(VARIANT, "w", encoding="utf-8") as f:
                f.write("")
            print("[revert] appended line removed, variant back to the factory baseline.")
    elif cmd == "status":
        print(f"Variant file: {VARIANT}")
        print(f"Appended line: {extra!r}" if extra else "Appended line: none (factory baseline)")
        print(f"Patch line: {'applied' if extra == patch else 'not applied'}")
    else:  # gate
        if not (os.environ.get("MODEL_BASE_URL") or os.environ.get("MODEL_FAKE")):
            sys.exit("Model API required, set MODEL_BASE_URL / MODEL_NAME.\n"
                     "Without a model API the gate cannot replay (MODEL_FAKE only fits pre-scripted teaching traces).")
        if extra:
            agent.SYSTEM = agent.SYSTEM + "\n" + extra  # seam, same consumption path as labs/ch06
        print(f"[gate] system prompt = factory SYSTEM"
              + (f" + appended line {extra!r}" if extra else " (baseline)") + ", running the ci/gate replay layer ...")
        sys.path.insert(0, os.path.join(ROOT, "ci"))
        import gate  # noqa: E402
        gate.main(os.path.join(ROOT, "ci", "gate.yaml"))


if __name__ == "__main__":
    main()
