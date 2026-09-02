import datetime
import html
import json
import os
import sys
import urllib.request


TOKEN = os.environ["GH_TOKEN"]
USER = os.environ.get("GH_USER", "ItsKaiross")
OUTPUT_PATH = ".github/badges/contribution-graph.svg"


def gql(query, variables):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "ItsKaiross-contribution-graph",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.load(response)
    if body.get("errors"):
        print(f"::error::GraphQL error: {body['errors']}", file=sys.stderr)
        sys.exit(1)
    return body["data"]


query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          firstDay
          contributionDays { date contributionCount weekday }
        }
      }
    }
  }
}
"""

today = datetime.datetime.now(datetime.timezone.utc).date()
start = today - datetime.timedelta(days=364)
data = gql(
    query,
    {
        "login": USER,
        "from": f"{start.isoformat()}T00:00:00Z",
        "to": f"{today.isoformat()}T23:59:59Z",
    },
)
user = data.get("user")
if user is None:
    print(f"::error::GitHub user '{USER}' was not found", file=sys.stderr)
    sys.exit(1)

calendar = user["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"][-53:]
positive_counts = sorted(
    day["contributionCount"]
    for week in weeks
    for day in week["contributionDays"]
    if day["contributionCount"] > 0
)


def quartile(index):
    if not positive_counts:
        return 1
    return positive_counts[round((len(positive_counts) - 1) * index / 4)]


thresholds = [quartile(i) for i in range(1, 5)]
colors = ["#25263a", "#3f3a78", "#6259bb", "#00a97f", "#00c896"]


def level(count):
    if count == 0:
        return 0
    for index, threshold in enumerate(thresholds, start=1):
        if count <= threshold:
            return index
    return 4


width = 900
height = 188
left = 46
top = 57
cell = 11
gap = 4
step = cell + gap

parts = [
    f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">',
    f'<title id="title">{html.escape(USER)} contribution graph</title>',
    f'<desc id="desc">{calendar["totalContributions"]} contributions in the last year.</desc>',
    f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="#1a1b27" stroke="#33344a"/>',
    '<g font-family="Segoe UI, Ubuntu, sans-serif">',
    f'<text x="24" y="28" fill="#ffffff" font-size="16" font-weight="700">Contribution Graph</text>',
    f'<text x="876" y="28" fill="#8b8fa3" font-size="12" text-anchor="end">{calendar["totalContributions"]} contributions in the last year</text>',
]

month_labels = []
last_month = None
for week_index, week in enumerate(weeks):
    first_day = datetime.date.fromisoformat(week["firstDay"])
    middle = first_day + datetime.timedelta(days=3)
    if middle.month != last_month:
        month_labels.append((left + week_index * step, middle.strftime("%b")))
        last_month = middle.month

for x, label in month_labels:
    parts.append(f'<text x="{x}" y="47" fill="#8b8fa3" font-size="10">{label}</text>')

for weekday, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    y = top + weekday * step + 9
    parts.append(f'<text x="38" y="{y}" fill="#8b8fa3" font-size="9" text-anchor="end">{label}</text>')

for week_index, week in enumerate(weeks):
    x = left + week_index * step
    for day in week["contributionDays"]:
        date = datetime.date.fromisoformat(day["date"])
        if date > today:
            continue
        count = day["contributionCount"]
        y = top + day["weekday"] * step
        noun = "contribution" if count == 1 else "contributions"
        tooltip = html.escape(f"{count} {noun} on {date.strftime('%b %d, %Y')}")
        parts.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level(count)]}"><title>{tooltip}</title></rect>'
        )

legend_x = 757
parts.append(f'<text x="{legend_x - 8}" y="174" fill="#8b8fa3" font-size="9" text-anchor="end">Less</text>')
for index, color in enumerate(colors):
    parts.append(f'<rect x="{legend_x + index * 15}" y="165" width="11" height="11" rx="2" fill="{color}"/>')
parts.append(f'<text x="{legend_x + 82}" y="174" fill="#8b8fa3" font-size="9">More</text>')
parts.extend(["</g>", "</svg>"])

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as output:
    output.write("\n".join(parts) + "\n")

print(f"Generated {OUTPUT_PATH} with {calendar['totalContributions']} contributions")
