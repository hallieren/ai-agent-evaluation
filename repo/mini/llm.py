"""The only file in the whole repo that touches a model API.

Vendor-neutral: configured via environment variables; any OpenAI-compatible endpoint works.
  MODEL_BASE_URL  e.g. https://api.example.com/v1
  MODEL_NAME      model name
  MODEL_API_KEY   API key (optional for local endpoints)
Offline mode: with MODEL_FAKE=1, replies come from a scripted queue (for tests and teaching-trace generation).
"""
import json
import os
import time
import urllib.error
import urllib.request

_script = []  # scripted queue for fake mode


def set_script(responses):
    """responses: [{"content": str, "tool_calls": [{"name","args"}]}, ...]"""
    _script.clear()
    _script.extend(responses)


def chat(messages, tools=None):
    """Returns {"content", "tool_calls", "usage": {"tokens_in", "tokens_out"}}"""
    if os.environ.get("MODEL_FAKE"):
        return _fake(messages)
    assert os.environ.get("MODEL_BASE_URL") and os.environ.get("MODEL_NAME"), \
        "Model API not configured: export MODEL_BASE_URL / MODEL_NAME first (MODEL_API_KEY optional), see the repo README"
    body = {"model": os.environ["MODEL_NAME"], "messages": messages}
    if tools:
        body["tools"] = [{"type": "function", "function": t} for t in tools]
    req = urllib.request.Request(
        os.environ["MODEL_BASE_URL"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ.get("MODEL_API_KEY", "")})
    # timeout + bounded retries: a network call with no timeout silently hangs the whole eval suite
    data, last_err = None, None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.load(resp)
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
    if data is None:
        raise RuntimeError(f"Model API failed 3 times in a row (last error: {last_err})")
    msg = data["choices"][0]["message"]
    calls = [{"name": c["function"]["name"], "args": json.loads(c["function"]["arguments"])}
             for c in msg.get("tool_calls") or []]
    usage = data.get("usage", {})
    return {"content": msg.get("content") or "", "tool_calls": calls,
            "usage": {"tokens_in": usage.get("prompt_tokens", 0),
                      "tokens_out": usage.get("completion_tokens", 0)}}


def _fake(messages):
    assert _script, "MODEL_FAKE=1 but the script queue is empty: call set_script() first"
    r = _script.pop(0)
    tokens_in = sum(len(str(m.get("content", ""))) for m in messages) // 4
    tokens_out = (len(r.get("content", "")) + 20 * len(r.get("tool_calls", []))) // 4
    return {"content": r.get("content", ""), "tool_calls": r.get("tool_calls", []),
            "usage": {"tokens_in": tokens_in, "tokens_out": tokens_out}}


def cost_usd(tokens_in, tokens_out):
    """Illustrative USD figure: unit prices are set via environment variables; defaults are teaching placeholders."""
    pin = float(os.environ.get("MODEL_USD_PER_1K_IN", "0.001"))
    pout = float(os.environ.get("MODEL_USD_PER_1K_OUT", "0.003"))
    return round(tokens_in / 1000 * pin + tokens_out / 1000 * pout, 6)
