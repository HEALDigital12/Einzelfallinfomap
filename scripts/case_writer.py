import json
from pathlib import Path
from datetime import datetime, timezone


def read_json(path, default):
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def merge_cases(old_cases, new_cases):
    seen = {c.get("source_url") for c in old_cases if c.get("source_url")}
    merged = list(old_cases)
    added = 0
    for case in new_cases:
        url = case.get("source_url")
        if url and url not in seen:
            merged.append(case)
            seen.add(url)
            added += 1
    return merged, added


def write_month(year, month, cases):
    out = f"public/data/backfill/faelle_{year}_{month:02d}.json"
    data = read_json(out, {"cases": []})
    merged, added = merge_cases(data.get("cases", []), cases)
    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "year": year,
        "month": month,
        "count": len(merged),
        "added": added,
        "cases": merged,
    }
    write_json(out, data)
    return out, added, len(merged)
