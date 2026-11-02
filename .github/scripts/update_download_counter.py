#!/usr/bin/env python3
"""Aggiorna il contatore dei download nel README.

GitHub fornisce solo il totale di ogni file, senza date: i conteggi su 7 e 30
giorni si ricavano dai totali salvati in .github/download-stats.json. Lì si
aggiunge una riga solo quando un totale cambia, così il sito non viene
ripubblicato ogni giorno senza motivo.
"""
import datetime
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATS_FILE = ROOT / ".github" / "download-stats.json"
README_FILE = ROOT / "README.md"

# Si contano solo i file che installano l'app, non appcast, firme e checksum.
PLATFORMS = [
    {"key": "mac", "label": "Mac", "repo": "frabolla/unwrap-macOS-release", "suffix": ".dmg"},
    {"key": "windows", "label": "Windows", "repo": "frabolla/unwrap-win-release", "suffix": "Setup.exe"},
]
WINDOWS_DAYS = [7, 30]
COLLECTING = "in raccolta"
START_MARKER = "<!-- download-counter:start -->"
END_MARKER = "<!-- download-counter:end -->"


def fetch_total(repo, suffix):
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    total = 0
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=100&page={page}"
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
            releases = json.load(response)
        if not releases:
            return total
        for release in releases:
            for asset in release["assets"]:
                if asset["name"].endswith(suffix):
                    total += asset["download_count"]
        page += 1


def record_snapshot(snapshots, today, totals):
    """Aggiunge i totali di oggi, se diversi dall'ultima rilevazione."""
    snapshot = {"date": today.isoformat(), **totals}
    if not snapshots:
        return [snapshot]
    last = snapshots[-1]
    if all(last[key] == value for key, value in totals.items()):
        return snapshots
    if last["date"] == snapshot["date"]:
        return snapshots[:-1] + [snapshot]
    return snapshots + [snapshot]


def downloads_in_window(snapshots, today, days, keys):
    """Download negli ultimi `days` giorni, None se la raccolta è troppo recente."""
    cutoff = (today - datetime.timedelta(days=days)).isoformat()
    baseline = None
    for snapshot in snapshots:
        if snapshot["date"] <= cutoff:
            baseline = snapshot
    if baseline is None:
        return None
    current = snapshots[-1]
    # Eliminare una release può far scendere il totale: il conteggio non va sotto zero.
    return max(sum(current[key] - baseline[key] for key in keys), 0)


def render_table(snapshots, today):
    rows = [(platform["label"], [platform["key"]]) for platform in PLATFORMS]
    rows.append(("**Totale**", [platform["key"] for platform in PLATFORMS]))
    lines = ["| | Ultimi 7 giorni | Ultimi 30 giorni | Dall'inizio |", "|---|---:|---:|---:|"]
    for label, keys in rows:
        cells = []
        for days in WINDOWS_DAYS:
            count = downloads_in_window(snapshots, today, days, keys)
            cells.append(COLLECTING if count is None else str(count))
        cells.append(str(sum(snapshots[-1][key] for key in keys)))
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def update_readme(readme, table):
    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    # Le righe vuote evitano che Markdown legga il marcatore finale come riga della tabella.
    block = f"{START_MARKER}\n\n{table}\n\n{END_MARKER}"
    return re.sub(pattern, lambda _: block, readme, flags=re.DOTALL)


def main():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    totals = {p["key"]: fetch_total(p["repo"], p["suffix"]) for p in PLATFORMS}

    snapshots = []
    if STATS_FILE.exists():
        snapshots = json.loads(STATS_FILE.read_text())["snapshots"]
    snapshots = record_snapshot(snapshots, today, totals)
    STATS_FILE.write_text(json.dumps({"snapshots": snapshots}, indent=2) + "\n")

    table = render_table(snapshots, today)
    README_FILE.write_text(update_readme(README_FILE.read_text(), table))
    print(table)


if __name__ == "__main__":
    main()
