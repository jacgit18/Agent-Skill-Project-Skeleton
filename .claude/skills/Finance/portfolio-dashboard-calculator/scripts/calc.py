#!/usr/bin/env python3
"""Portfolio dashboard calculator (no UI). Same rules as the dashboard, run from chat.

Usage:  python3 calc.py <command> '<json>'      (or pipe JSON on stdin)
Commands: split | drift | held | stress | monthly | trade | rank | full
Every result is JSON. Money is in dollars in the output; internally the plan math uses integer cents.
Nothing here recommends anything: it returns arithmetic on the numbers it is given.
"""
import json
import math
import sys

CLASSES = [
    {"id": "re", "name": "Real estate", "pct": 50, "band": 5, "moderate": -10, "severe": -25,
     "subs": [("REITs", 25), ("Direct property", 25), ("Crowdfunding platforms", 25), ("Development projects", 25)]},
    {"id": "cs", "name": "Company stocks", "pct": 15, "band": 3, "moderate": -20, "severe": -40,
     "subs": [("Blue-chip companies", 100 / 3), ("Dividend payers", 100 / 3), ("Growth stocks", 100 / 3)]},
    {"id": "etf", "name": "Stock ETFs", "pct": 15, "band": 3, "moderate": -15, "severe": -35,
     "subs": [("Index ETFs (S&P 500, Nasdaq)", 25), ("Sector ETFs", 25), ("International ETFs", 25), ("Dividend ETFs", 25)]},
    {"id": "spec", "name": "Speculative", "pct": 18, "band": 3, "moderate": -35, "severe": -60,
     "subs": [("Cryptocurrency", 50), ("Startup investments", 50)]},
    {"id": "gold", "name": "Gold", "pct": 2, "band": 1, "moderate": 5, "severe": 10,
     "subs": [("Physical gold", 100 / 3), ("Gold ETFs", 100 / 3), ("Gold mining stocks", 100 / 3)]},
]
SPEC_THREE = [("Cryptocurrency", 100 / 3), ("Startup investments", 100 / 3), ("High-risk stocks", 100 / 3)]
IDS = [c["id"] for c in CLASSES]
EPS = 1e-9


def money(x):
    x = round(x + 0.0, 2)
    s = f"{abs(x):,.0f}" if x == int(x) else f"{abs(x):,.2f}"
    return ("-" if x < 0 else "") + "$" + s


def pct(x):
    return f"{round(x, 2):g}"


def rnd(x):  # round half up, like the dashboard
    return math.floor(x + 0.5)


def allocate(total_cents, pcts):
    """Largest-remainder split so pieces add up exactly."""
    raw = [total_cents * p / 100 for p in pcts]
    out = [math.floor(r + 1e-7) for r in raw]
    rem = int(round(sum(raw))) - sum(out)
    order = sorted(range(len(raw)), key=lambda i: -(raw[i] - out[i]))
    for i in order[:max(0, rem)]:
        out[i] += 1
    return out


def cents(d):
    return int(rnd(float(d or 0) * 100))


def dollars(c):
    return c / 100


def norm_pcts(targets):
    t = sum(targets)
    return [x / t * 100 for x in targets] if t > 0 else [0] * len(targets)


def targets_from(d):
    t = d.get("targets")
    if t:
        return [float(t.get(i, 0)) for i in IDS]
    return [float(c["pct"]) for c in CLASSES]


def cmd_split(d):
    cap = cents(d.get("capital", 23000))
    tg = targets_from(d)
    amts = allocate(cap, tg)
    rows = []
    for i, c in enumerate(CLASSES):
        subs = c["subs"]
        if c["id"] == "spec" and d.get("spec_mode") == "three":
            subs = SPEC_THREE
        sp = d.get("subs", {}).get(c["id"])
        pcts = [float(x) for x in sp] if sp else [p for _, p in subs]
        sub_amts = allocate(amts[i], pcts)
        rows.append({"class": c["name"], "pct": tg[i], "amount": dollars(amts[i]),
                     "text": f"{c['name']} {pct(tg[i])}%: {money(dollars(amts[i]))}",
                     "subs": [{"name": n, "pct_of_class": p, "amount": dollars(a)} for (n, _), p, a in zip(subs, pcts, sub_amts)]})
    total = sum(tg)
    return {"capital": dollars(cap), "classes": rows, "sum_pct": total,
            "note": None if abs(total - 100) < 0.05 else f"Targets add up to {pct(total)}%, not 100%."}


def cmd_drift(d):
    tg = targets_from(d)
    norm = norm_pcts(tg)
    cur = [cents(d.get("holdings", {}).get(i, 0)) for i in IDS]
    M = cents(d.get("new_money", 0))
    T = sum(cur)
    base = T + M
    target = allocate(base, norm)
    mode = d.get("mode", "rebalance")
    notes = []
    if sum(tg) <= 0:
        notes.append("Set target percentages to see drift.")
    elif abs(sum(tg) - 100) > 0.05:
        notes.append(f"Targets add up to {pct(sum(tg))}%, so they are scaled to 100% here.")
    if mode == "new_money":
        deficits = [max(0, target[i] - cur[i]) for i in range(5)]
        if M == 0:
            trade = [0] * 5
            notes.append("Enter an amount of new money to see where it should go.")
        else:
            weights = norm_pcts(deficits) if sum(deficits) > 0 else norm
            trade = allocate(M, weights)
    else:
        trade = [target[i] - cur[i] for i in range(5)]
    bands = {c["id"]: c["band"] for c in CLASSES}
    bands.update(d.get("bands", {}))
    rows, out_of_band = [], 0
    for i, c in enumerate(CLASSES):
        row = {"class": c["name"], "target": dollars(target[i]), "current": dollars(cur[i]), "trade": dollars(trade[i])}
        if T > 0 and sum(tg) > 0:
            cp = cur[i] / T * 100
            drift = cp - norm[i]
            status = "In band" if abs(drift) <= float(bands[c["id"]]) + 1e-9 else ("Over" if drift > 0 else "Under")
            out_of_band += status != "In band"
            row.update({"current_pct": cp, "target_pct": norm[i], "drift_pts": drift, "band": float(bands[c["id"]]), "status": status})
        after = cur[i] + trade[i]
        row["after"] = dollars(after)
        row["after_pct"] = after / base * 100 if base else 0
        row["action"] = ("Buy " + money(dollars(trade[i]))) if trade[i] > 0 else (("Sell " + money(dollars(-trade[i]))) if trade[i] < 0 else "No trade")
        rows.append(row)
    summ = (f"Holdings total {money(dollars(T))}. New money {money(dollars(M))}. {out_of_band} of 5 classes outside their band."
            if T > 0 else "Enter your current holdings to see drift.")
    return {"mode": mode, "holdings_total": dollars(T), "new_money": dollars(M), "rows": rows, "summary": summ, "notes": notes}


def cmd_held(d):
    """Compare dollars assigned to accounts with each class's target dollars."""
    cap = cents(d.get("capital", 23000))
    target = allocate(cap, targets_from(d))
    assigned = d.get("assigned", {})
    rows = []
    for i, c in enumerate(CLASSES):
        a = sum(cents(v) for v in assigned.get(c["id"], {}).values())
        gap = target[i] - a
        rows.append({"class": c["name"], "target": dollars(target[i]), "assigned": dollars(a),
                     "tag": "Matches" if gap == 0 else (f"{money(dollars(gap))} unassigned" if gap > 0 else f"{money(dollars(-gap))} over")})
    return {"rows": rows}


def cmd_stress(d):
    cap = cents(d.get("capital", 23000))
    base = d.get("base", "target")
    if base == "current":
        vals = [cents(d.get("holdings", {}).get(i, 0)) for i in IDS]
    else:
        vals = allocate(cap, targets_from(d))
    sc = d.get("scenario", "moderate")
    shocks = {c["id"]: c.get(sc, 0) for c in CLASSES} if sc in ("moderate", "severe") else {}
    shocks.update(d.get("shocks", {}))
    change = [rnd(vals[i] * float(shocks.get(IDS[i], 0)) / 100) for i in range(5)]
    total, chg = sum(vals), sum(change)
    losses = sum(-x for x in change if x < 0)
    rows = [{"class": CLASSES[i]["name"], "value": dollars(vals[i]), "move_pct": float(shocks.get(IDS[i], 0)), "change": dollars(change[i]),
             "after": dollars(vals[i] + change[i]),
             "share_of_losses_pct": (-change[i] / losses * 100) if change[i] < 0 and losses else None} for i in range(5)]
    out = {"scenario": sc, "base": base, "rows": rows, "total_now": dollars(total), "total_change": dollars(chg),
           "total_after": dollars(total + chg), "total_change_pct": (chg / total * 100) if total else 0,
           "note": "Scenarios you set, not forecasts; every class moves at once by exactly these amounts."}
    if base == "current" and total == 0:
        out["note"] = "No current holdings entered, so there is nothing to stress."
    lim = d.get("loss_limit")
    if lim not in (None, "") and total > 0:
        loss_pct = -out["total_change_pct"] if chg < 0 else 0
        over = loss_pct - float(lim)
        out["limit"] = {"limit_pct": float(lim), "status": "Over limit" if over > 1e-9 else "Within limit",
                        "points_over": max(0, over), "approx_dollars_over": max(0, over) / 100 * dollars(total)}
    return out


def cmd_monthly(d):
    m = cents(d.get("monthly", 0))
    n = max(1, min(120, int(d.get("months", 12) or 1)))
    norm = norm_pcts(targets_from(d))
    mode = d.get("mode", "targets")
    bal = [cents(d.get("holdings", {}).get(i, 0)) for i in IDS]
    start = list(bal)
    total = [0] * 5
    if mode == "targets" or sum(bal) == 0:
        first = allocate(m, norm)
        total = [x * n for x in first]
    else:
        first = None
        for k in range(n):
            target = allocate(sum(bal) + m, norm)
            deficits = [max(0, target[i] - bal[i]) for i in range(5)]
            w = norm_pcts(deficits) if sum(deficits) > 0 else norm
            buy = allocate(m, w)
            if k == 0:
                first = buy
            bal = [bal[i] + buy[i] for i in range(5)]
            total = [total[i] + buy[i] for i in range(5)]
    after = [start[i] + total[i] for i in range(5)]
    at = sum(after)
    return {"mode": mode, "monthly": dollars(m), "months": n, "total_added": dollars(sum(total)),
            "rows": [{"class": CLASSES[i]["name"], "month_1": dollars(first[i]), "over_n_months": dollars(total[i]),
                      "balance_after": dollars(after[i]), "share_after_pct": after[i] / at * 100 if at else 0} for i in range(5)],
            "summary": f"{money(dollars(m))} a month for {n} months adds {money(dollars(sum(total)))} in total. No market returns assumed.",
            "note": "No current holdings entered, so this matches By target %." if mode != "targets" and sum(start) == 0 else None}


def cmd_trade(d):
    acct = float(d.get("account", 10000))
    risk = float(d.get("risk_pct", 2))
    entry = float(d.get("entry", 25))
    stop = float(d["stop"]) if d.get("stop") not in (None, "") else round(entry * (1 - float(d.get("stop_pct", 15)) / 100), 4)
    target = float(d["target"]) if d.get("target") not in (None, "") else round(entry * (1 + float(d.get("target_pct", 40)) / 100), 4)
    min_rr = float(d.get("min_rr", 2))
    budget = acct * risk / 100
    per, gain = entry - stop, target - entry
    flags, ok = [], False
    if acct <= 0:
        flags.append("Enter your account size.")
    elif risk <= 0:
        flags.append("Enter the percentage of the account you will risk.")
    elif entry <= 0:
        flags.append("Enter an entry price.")
    elif stop <= 0:
        flags.append("Enter a stop price.")
    elif per <= 0:
        flags.append("The stop must be below the entry: risk per share is zero or negative, so no size is possible.")
    else:
        ok = True
    out = {"account": acct, "risk_pct": risk, "risk_budget": budget, "entry": entry, "stop": stop, "target": target,
           "min_rr": min_rr, "valid": ok, "flags": flags}
    if ok:
        rr = gain / per
        shares = max(0, math.floor(budget / per + EPS))   # rounds down: planned loss never exceeds the budget
        pos = shares * entry
        out.update({"risk_per_share": per, "profit_per_share": gain, "rr": rr, "shares": shares, "position_value": pos,
                    "pct_deployed": pos / acct * 100, "max_loss": shares * per, "estimated_profit": shares * gain})
        if gain <= 0:
            flags.append("The target is at or below the entry, so there is no reward to measure.")
        elif rr < min_rr - EPS:
            flags.append(f"Reward:risk of {rr:.2f}x is below your {pct(min_rr)}x minimum.")
        else:
            flags.append(f"Reward:risk of {rr:.2f}x clears your {pct(min_rr)}x minimum.")
        if shares == 0:
            flags.append("The risk budget is too small for even one share at this stop distance.")
        if pos > acct + EPS:
            flags.append("This position costs more than the account holds, so it would need margin.")
        if risk > 3:
            flags.append(f"Risking {pct(risk)}% is above the 1 to 3% risk-per-trade range.")
        flags.append("A stop is not a guaranteed exit price; a gap or fast market can fill worse.")
    return out


def cmd_rank(d):
    acct = float(d.get("account", 10000))
    risk = float(d.get("risk_pct", 2))
    min_rr = float(d.get("min_rr", 2))
    equal = d.get("weight", "rr") == "equal"
    budget = acct * risk / 100
    items = []
    for i, c in enumerate(d.get("candidates", [])[:30]):
        t = "".join(ch for ch in str(c.get("ticker", "")).upper() if ch.isalnum() or ch in ".-").lstrip(".-")[:12]
        e, s, g = float(c.get("entry", 0) or 0), float(c.get("stop", 0) or 0), float(c.get("target", 0) or 0)
        per, gain = e - s, g - e
        valid = bool(t) and e > 0 and s > 0 and per > 0 and gain > 0
        items.append({"i": i, "ticker": t, "entry": e, "stop": s, "target": g, "valid": valid, "per": per, "rr": gain / per if valid else 0})
    valid = sorted([x for x in items if x["valid"]], key=lambda x: (-x["rr"], x["i"]))
    wsum = sum(1 if equal else x["rr"] for x in valid)
    for k, x in enumerate(valid):
        x["rank"] = k + 1
        x["risk_dollars"] = budget * (1 if equal else x["rr"]) / wsum if wsum else 0
        x["shares"] = max(0, math.floor(x["risk_dollars"] / x["per"] + EPS))
        x["position_value"] = x["shares"] * x["entry"]
    deployed = sum(x["position_value"] for x in valid)
    cleared = sum(1 for x in valid if x["rr"] >= min_rr - EPS)
    flags = []
    if acct > 0 and deployed > acct + EPS:
        flags.append(f"Combined position value of {money(deployed)} is more than the {money(acct)} account, so it would need margin.")
    excluded = [x["ticker"] for x in items if not x["valid"] and x["ticker"]]
    if excluded:
        flags.append(f"Excluded (need entry, a stop below it, a target above it): {', '.join(excluded)}.")
    keep = ("rank", "ticker", "entry", "stop", "target", "rr", "risk_dollars", "shares", "position_value")
    return {"risk_budget": budget, "weight": "equal" if equal else "rr", "ranked": [{k: x[k] for k in keep} for x in valid],
            "deployed": deployed, "clear_minimum": cleared, "excluded": excluded, "flags": flags,
            "summary": f"Total risk budget {money(budget)}. {len(valid)} candidates, {money(deployed)} deployed. "
                       f"{cleared} of {len(valid)} clear the {pct(min_rr)}x minimum.",
            "note": "Reward:risk arithmetic on the numbers given. It says nothing about whether a stock is a good investment."}


def cmd_full(d):
    out = {"split": cmd_split(d)}
    if d.get("holdings"):
        out["drift"] = cmd_drift(d)
    if d.get("assigned"):
        out["held"] = cmd_held(d)
    out["stress"] = cmd_stress(d)
    if d.get("monthly"):
        out["monthly"] = cmd_monthly(d)
    if d.get("trade"):
        out["trade"] = cmd_trade(d["trade"])
    if d.get("candidates"):
        r = dict(d.get("trade") or {})
        r["candidates"] = d["candidates"]
        out["rank"] = cmd_rank(r)
    return out


CMDS = {"split": cmd_split, "drift": cmd_drift, "held": cmd_held, "stress": cmd_stress, "monthly": cmd_monthly,
        "trade": cmd_trade, "rank": cmd_rank, "full": cmd_full}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit("usage: calc.py <" + "|".join(CMDS) + "> '<json>'")
    raw = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
    print(json.dumps(CMDS[sys.argv[1]](json.loads(raw or "{}")), indent=2, default=float))
