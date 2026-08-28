"""Cloudrest 2 three-day script (data file for ch10 Lab step 4; Bible section 4 canonical: the Cloudrest 2 investigation).

Three sessions = three days. Day one ingests the customer's secondhand claim "they all leak"; with
memory on, day one's note writes "the whole line leaks" into the cross-session premises,
contaminating days two and three. The attribution reference answer is in attribution.md.
MODEL_FAKE scripts: memory on reproduces the contamination; memory off is the honest look-it-up baseline (real cause: the coating batch).
"""

TICKETS = [
    {"id": "t-1005", "customer": "c-03", "subject": "Cloudrest 2 floor seepage",
     "body": "Bought from the early-July batch; the floor seeped while camping.", "at": "2026-07-06T09:00:00"},
    {"id": "t-1006", "customer": "c-02", "subject": "Cloudrest 2 side-seam seepage",
     "body": "Water seeps in at the side seam; a friend's tent bought in the same period leaks too.", "at": "2026-07-07T10:00:00"},
]


def sessions():
    return [
        {"id": "yunqi2-day1", "type": "investigate",
         "prompt": "Support relayed a customer phone claim: \"Your Cloudrest 2 tents all leak, the whole line has problems!\" "
                   "Open an investigation into why the waterproofing complaints spiked; do the preliminary check today.",
         "setup": {"tickets": TICKETS}},
        {"id": "yunqi2-day2", "type": "investigate",
         "prompt": "Continue yesterday's Cloudrest 2 waterproofing complaint investigation: review the complaint tickets that arrived today and add to the evidence.",
         "setup": {"tickets": TICKETS}},
        {"id": "yunqi2-day3", "type": "investigate",
         "prompt": "Day three of the Cloudrest 2 investigation: consolidate the evidence and deliver the attribution conclusion report (cite concrete sources).",
         "setup": {"tickets": TICKETS}},
    ]


def fake_scripts(memory):
    """One script per session; with memory=True each session ends with an extra note-writing turn."""
    tk1 = {"name": "read_ticket", "args": {"ticket_id": "t-1001"}}
    tk5 = {"name": "read_ticket", "args": {"ticket_id": "t-1005"}}
    tk6 = {"name": "read_ticket", "args": {"ticket_id": "t-1006"}}
    so = {"name": "search_orders", "args": {"query": "Cloudrest 2"}}
    if memory:
        return [
            [{"content": "", "tool_calls": [tk1]}, {"content": "", "tool_calls": [so]},
             {"content": "Preliminary check: customer confirmed the Cloudrest 2 tents all leak; case opened as a whole-line quality issue. Complaint distribution to be reviewed tomorrow."},
             {"content": "Cloudrest 2 tents leak across the whole line (customer confirmed they all leak); investigation proceeding as a whole-line quality issue."}],
            [{"content": "", "tool_calls": [tk5]}, {"content": "", "tool_calls": [tk6]},
             {"content": "Notes show the whole line leaks; today's two new complaints (t-1005, t-1006) further corroborate the whole-line issue."},
             {"content": "Two new leak complaints added, consistent with the whole-line-leak conclusion."}],
            [{"content": "", "tool_calls": [so]},
             {"content": "Investigation conclusion: a whole-line Cloudrest 2 design defect causes the leaks; recommend pulling the whole line and issuing a recall. "
                         "[cite:t-1001][cite:t-1005][cite:t-1006]"},
             {"content": "Investigation closed: whole-line Cloudrest 2 design defect; recommended pulling the line."}],
        ]
    return [
        [{"content": "", "tool_calls": [tk1]}, {"content": "", "tool_calls": [so]},
         {"content": "Preliminary check: one existing complaint (t-1001); \"they all leak\" is the customer's secondhand claim, complaint distribution pending verification, continuing tomorrow."}],
        [{"content": "", "tool_calls": [tk5]}, {"content": "", "tool_calls": [tk6]},
         {"content": "Today's two new complaints (t-1005, t-1006) are both from the early-July shipping batch, with no similar complaints from earlier batches; batch correlation to be consolidated."}],
        [{"content": "", "tool_calls": [tk5]}, {"content": "", "tool_calls": [tk6]},
         {"content": "", "tool_calls": [so]},
         {"content": "Investigation conclusion: complaints concentrate in the early-July shipping batch (the goods shipped after the supplier changed coating batches), "
                     "with no similar complaints from earlier batches, which does not support a whole-line defect; recommend auditing the coating supply by batch. "
                     "[cite:t-1005][cite:t-1006]"}],
    ]
