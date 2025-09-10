from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent
STATE_FILE = ROOT / ".timer_state.json"
LOG_FILE = ROOT / "sessions.csv"

def now() -> datetime:
    return datetime.now()

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"running": False, "start_ts": None, "label": "", "target_ts": None}

def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def ensure_log_header():
    if not LOG_FILE.exists():
        LOG_FILE.write_text("start,end,minutes,label\n", encoding="utf-8")

def log_session(start: datetime, end: datetime, label: str):
    ensure_log_header()
    minutes = round((end - start).total_seconds() / 60, 2)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{fmt(start)},{fmt(end)},{minutes},{label}\n")

def cmd_start(args):
    state = load_state()
    if state["running"]:
        print("A session is already running. Use: status or stop")
        return 1
    mins = args.minutes
    label = args.label or "focus"
    start = now()
    target = start + timedelta(minutes=mins)
    state.update({
        "running": True,
        "start_ts": fmt(start),
        "target_ts": fmt(target),
        "label": label
    })
    save_state(state)
    print(f"✅ Started {mins} min session ({label}) at {fmt(start)}; ends ~ {fmt(target)}")
    return 0

def cmd_status(_args):
    state = load_state()
    if not state["running"]:
        print("No session running. Start one with: start --minutes 25 --label work")
        return 0
    start = parse_dt(state["start_ts"])
    target = parse_dt(state["target_ts"])
    remaining = target - now()
    if remaining.total_seconds() <= 0:
        print("⏰ Timer should have ended. Run: stop (to log it).")
    else:
        mins = int(remaining.total_seconds() // 60)
        secs = int(remaining.total_seconds() % 60)
        print(f"🟢 Running ({state['label']}) — time left: {mins:02d}:{secs:02d}")
    return 0

def cmd_stop(_args):
    state = load_state()
    if not state["running"]:
        print("No active session.")
        return 1
    start = parse_dt(state["start_ts"])
    end = now()
    label = state.get("label", "focus")
    log_session(start, end, label)
    state.update({"running": False, "start_ts": None, "target_ts": None, "label": ""})
    save_state(state)
    print(f"🧾 Logged session: {fmt(start)} → {fmt(end)} ({label})")
    return 0

def cmd_log(_args):
    if not LOG_FILE.exists():
        print("No sessions yet.")
        return 0
    print(LOG_FILE.read_text(encoding="utf-8"))
    return 0

def cmd_stats(_args):
    if not LOG_FILE.exists():
        print("No sessions yet.")
        return 0
    total_min = 0.0
    by_day: dict[str, float] = {}
    with LOG_FILE.open(encoding="utf-8") as f:
        next(f, None)  # skip header
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(",")
            if len(parts) < 4:
                continue
            start_s, end_s, mins_s, label = parts[0], parts[1], parts[2], ",".join(parts[3:])
            try:
                minutes = float(mins_s)
                total_min += minutes
                day = start_s.split(" ")[0]
                by_day[day] = by_day.get(day, 0.0) + minutes
            except Exception:
                pass
    print(f"Total focus minutes: {round(total_min,2)}")
    if by_day:
        print("By day:")
        for day in sorted(by_day.keys()):
            print(f"  {day}: {round(by_day[day],2)}")
    return 0

def cmd_reset(_args):
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    print("State cleared. (sessions.csv untouched)")
    return 0

def build_parser():
    p = argparse.ArgumentParser(
        prog="focus-timer",
        description="CLI Pomodoro: start/stop sessions, status, CSV logs, stats."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="Start a session")
    s.add_argument("--minutes", "-m", type=int, default=25, help="Duration in minutes (default 25)")
    s.add_argument("--label", "-l", type=str, default="focus", help="Label for the session")
    s.set_defaults(func=cmd_start)

    st = sub.add_parser("status", help="Show remaining time")
    st.set_defaults(func=cmd_status)

    sp = sub.add_parser("stop", help="Stop and log the current session")
    sp.set_defaults(func=cmd_stop)

    lg = sub.add_parser("log", help="Print raw sessions.csv")
    lg.set_defaults(func=cmd_log)

    stats = sub.add_parser("stats", help="Show total minutes and per-day totals")
    stats.set_defaults(func=cmd_stats)

    rs = sub.add_parser("reset", help="Clear state (does not delete sessions.csv)")
    rs.set_defaults(func=cmd_reset)

    return p

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
