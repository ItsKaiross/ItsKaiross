import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ["GH_TOKEN"]
USER = os.environ["GH_USER"]

TEMPLATE_PATH = ".github/badges/commit-count-template.svg"
OUTPUT_PATH = ".github/badges/commit-count.svg"


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


created_at = gql(
    "query($login: String!) { user(login: $login) { createdAt } }",
    {"login": USER},
)["user"]["createdAt"]

today = datetime.now(timezone.utc).date()
start_year = int(created_at[:4])

commits_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
    }
  }
}
"""

total = 0
for year in range(start_year, today.year + 1):
    frm = created_at if year == start_year else f"{year}-01-01T00:00:00Z"
    to = (
        today.strftime("%Y-%m-%dT23:59:59Z")
        if year == today.year
        else f"{year}-12-31T23:59:59Z"
    )
    data = gql(commits_query, {"login": USER, "from": frm, "to": to})
    total += data["user"]["contributionsCollection"]["totalCommitContributions"]

template = open(TEMPLATE_PATH, encoding="utf-8").read()
template = template.replace("{{TOTAL}}", str(total))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(template)

print(json.dumps({"total_commits": total}, indent=2))
