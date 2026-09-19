#!/usr/bin/env python3
"""Checks calc.py against the dashboard's acceptance numbers. Run: python3 test_calc.py"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calc

fails = 0


def eq(name, got, want, tol=0.005):
    global fails
    if isinstance(want, list) and want and isinstance(want[0], (int, float)) and not isinstance(want[0], bool):
        ok = len(got) == len(want) and all(abs(a - b) <= tol for a, b in zip(got, want))
    else:
        ok = got == want
    if not ok:
        fails += 1
        print("FAIL", name, got, "expected", want)


H = {"re": 15000, "cs": 3000, "etf": 2500, "spec": 2000, "gold": 500}
s = calc.cmd_split({"capital": 23000})
eq("split defaults", [c["amount"] for c in s["classes"]], [11500, 3450, 3450, 4140, 460])
eq("thirds of 1000", [x / 100 for x in calc.allocate(100000, [100 / 3] * 3)], [333.34, 333.33, 333.33])
eq("gold subs at 1000", [x["amount"] for x in calc.cmd_split({"capital": 1000})["classes"][4]["subs"]], [6.67, 6.67, 6.66])
d = calc.cmd_drift({"holdings": H})
eq("rebalance trades", [r["trade"] for r in d["rows"]], [-3500, 450, 950, 2140, -40])
eq("statuses", [r["status"] for r in d["rows"]], ["Over", "In band", "Under", "Under", "In band"])
eq("drift summary", d["summary"], "Holdings total $23,000. New money $0. 3 of 5 classes outside their band.")
d = calc.cmd_drift({"holdings": H, "mode": "new_money", "new_money": 1000})
eq("new money only", [r["trade"] for r in d["rows"]], [0, 149.25, 273.63, 577.12, 0])
d = calc.cmd_drift({"new_money": 1000})
eq("no holdings", [r["trade"] for r in d["rows"]], [500, 150, 150, 180, 20])
st = calc.cmd_stress({})
eq("stress changes", [r["change"] for r in st["rows"]], [-1150, -690, -517.5, -1449, 23])
eq("stress total", [st["total_change"], round(st["total_change_pct"], 2), st["total_after"]], [-3783.5, -16.45, 19216.5])
eq("loss shares", [round(r["share_of_losses_pct"], 2) for r in st["rows"] if r["share_of_losses_pct"] is not None], [30.21, 18.13, 13.6, 38.07])
sv = calc.cmd_stress({"scenario": "severe", "loss_limit": 20})
eq("severe", [sv["total_change"], round(sv["limit"]["points_over"], 2), round(sv["limit"]["approx_dollars_over"], 2)], [-7900.5, 14.35, 3300.5])
m = calc.cmd_monthly({"monthly": 500, "months": 12})
eq("monthly month 1", [r["month_1"] for r in m["rows"]], [250, 75, 75, 90, 10])
eq("monthly total", [m["total_added"]], [6000])
m = calc.cmd_monthly({"monthly": 500, "months": 12, "mode": "catchup", "holdings": H})
eq("catch-up month 1", [r["month_1"] for r in m["rows"]], [0, 69.45, 135.58, 294.97, 0])
eq("catch-up total and balances", [m["total_added"], round(sum(r["balance_after"] for r in m["rows"]), 2)], [6000, 29000])
t = calc.cmd_trade({})
eq("trade defaults", [round(t["rr"], 2), t["shares"], t["position_value"], t["max_loss"], t["estimated_profit"]], [2.67, 53, 1325, 198.75, 530])
t = calc.cmd_trade({"account": 10000, "risk_pct": 2, "entry": 12, "stop": 10.5})
eq("worked example", [t["shares"], t["position_value"], t["max_loss"]], [133, 1596, 199.5])
t = calc.cmd_trade({"entry": 12, "stop": 10.6})
eq("rounds down", [t["shares"], round(t["max_loss"], 2)], [142, 198.8])
eq("stop = entry invalid", calc.cmd_trade({"entry": 10, "stop": 10})["valid"], False)
t = calc.cmd_trade({"account": 1000, "risk_pct": 50, "entry": 10, "stop": 9})
eq("margin and 3% warnings", [any("margin" in f for f in t["flags"]), any("above the 1 to 3%" in f for f in t["flags"])], [True, True])
C = [{"ticker": "AAPL", "entry": 25, "stop": 21.25, "target": 35}, {"ticker": "MSFT", "entry": 100, "stop": 90, "target": 130},
     {"ticker": "TSLA", "entry": 50, "stop": 45, "target": 55}, {"ticker": "BAD", "entry": 10, "stop": 12, "target": 20}]
r = calc.cmd_rank({"candidates": C})
eq("rank order", [x["ticker"] for x in r["ranked"]], ["MSFT", "AAPL", "TSLA"])
eq("rank shares", [x["shares"] for x in r["ranked"]], [9, 21, 6])
eq("rank summary", r["summary"], "Total risk budget $200. 3 candidates, $1,725 deployed. 2 of 3 clear the 2x minimum.")
eq("excluded", r["excluded"], ["BAD"])
r = calc.cmd_rank({"weight": "equal", "candidates": C[:3]})
eq("equal split", [x["shares"] for x in r["ranked"]], [6, 17, 13])
eq("ticker sanitised", calc.cmd_rank({"candidates": [{"ticker": "=HYPERLINK(x)", "entry": 10, "stop": 9, "target": 12}]})["ranked"][0]["ticker"], "HYPERLINKX")
eq("money format", [calc.money(862.5), calc.money(11500), calc.money(0.1)], ["$862.50", "$11,500", "$0.10"])
f = calc.cmd_full({"holdings": H, "monthly": 500, "trade": {"account": 10000}, "candidates": C})
eq("full has all sections", sorted(f), ["drift", "monthly", "rank", "split", "stress", "trade"]) if False else eq("full sections", sorted(f), ["drift", "monthly", "rank", "split", "stress", "trade"])
print("FAILED" if fails else "all passed")
sys.exit(1 if fails else 0)
