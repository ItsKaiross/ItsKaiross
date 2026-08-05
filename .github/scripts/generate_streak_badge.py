import datetime
import json
import os
import sys
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
USER = os.environ["GH_USER"]

TEMPLATE_PATH = ".github/badges/streak-stats-template.svg"
OUTPUT_PATH = ".github/badges/streak-stats.svg"


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
    if "errors" in body:
        print(f"::error::GraphQL error: {body['errors']}", file=sys.stderr)
        sys.exit(1)
    return body["data"]


def fmt(date_str, today):
    d = datetime.date.fromisoformat(date_str)
    return d.strftime("%b %-d, %Y") if d.year != today.year else d.strftime("%b %-d")


created_at = gql(
    "query($login: String!) { user(login: $login) { createdAt } }",
    {"login": USER},
)["user"]["createdAt"]

today = datetime.datetime.utcnow().date()
start_year = int(created_at[:4])

calendar_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

days = {}
for year in range(start_year, today.year + 1):
    frm = created_at if year == start_year else f"{year}-01-01T00:00:00Z"
    to = (
        today.strftime("%Y-%m-%dT23:59:59Z")
        if year == today.year
        else f"{year}-12-31T23:59:59Z"
    )
    data = gql(calendar_query, {"login": USER, "from": frm, "to": to})
    weeks = data["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    for week in weeks:
        for day in week["contributionDays"]:
            days[day["date"]] = day["contributionCount"]

sorted_dates = sorted(days)
total = sum(days.values())

longest = 0
longest_start = longest_end = None
run = 0
run_start = None
for d in sorted_dates:
    if days[d] > 0:
        if run == 0:
            run_start = d
        run += 1
        if run > longest:
            longest, longest_start, longest_end = run, run_start, d
    else:
        run = 0

today_str = today.isoformat()
i = len(sorted_dates) - 1
while i >= 0 and sorted_dates[i] > today_str:
    i -= 1
if i >= 0 and sorted_dates[i] == today_str and days[sorted_dates[i]] == 0:
    i -= 1  # today's contributions may not be reflected yet; grace period

current = 0
current_start = current_end = None
while i >= 0 and days[sorted_dates[i]] > 0:
    if current_end is None:
        current_end = sorted_dates[i]
    current_start = sorted_dates[i]
    current += 1
    i -= 1

template = open(TEMPLATE_PATH, encoding="utf-8").read()
replacements = {
    "{{TOTAL}}": str(total),
    "{{TOTAL_RANGE}}": f"{fmt(sorted_dates[0], today)} - Present" if sorted_dates else "",
    "{{CURRENT}}": str(current),
    "{{CURRENT_RANGE}}": (
        f"{fmt(current_start, today)} - {fmt(current_end, today)}" if current else "No streak yet"
    ),
    "{{LONGEST}}": str(longest),
    "{{LONGEST_RANGE}}": (
        f"{fmt(longest_start, today)} - {fmt(longest_end, today)}" if longest else ""
    ),
}
for placeholder, value in replacements.items():
    template = template.replace(placeholder, value)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(template)

print(json.dumps({k: v for k, v in replacements.items()}, indent=2))
