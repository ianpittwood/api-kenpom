# api-kenpom

An unofficial Python wrapper for kenpom.com's API.

## Installation

Requires Python 3.12+. Install with [uv](https://docs.astral.sh/uv/):

```bash
uv add api-kenpom
```

Or with pip:

```bash
pip install api-kenpom
```

## Usage

> [!NOTE]
> Some endpoints only work for 2010 or later.

```python
from kenpom import KenpomClient

client = KenpomClient(bearer_token="YOUR_API_KEY_HERE")

# Retrieve team ratings for the 2024-25 season
ratings = client.get_ratings(year=2025)

# Retrieve ratings for a single team (by team ID)
team = client.get_ratings(team_id=73)

# Retrieve ratings filtered by conference
acc = client.get_ratings(year=2025, conf="ACC")
```

## API Reference

### `KenpomClient(bearer_token)`

All methods return the decoded JSON response body (a `list` or `dict`).

| Method | Endpoint | Description |
|---|---|---|
| `get_ratings(year, team_id, conf)` | `ratings` | Team efficiency ratings, SOS, tempo, and possession length. At least one of `year` or `team_id` is required. |
| `get_ratings_archive_by_date(date, team_id, conf)` | `archive` | Historical ratings as of a specific date (`YYYY-MM-DD`). |
| `get_preseason_ratings_archive(year, team_id, conf)` | `archive` | Preseason ratings for a given year. |
| `get_four_factors(year, team_id, conf, conf_only)` | `four-factors` | Four factors statistics for offense and defense. |
| `get_point_distribution(year, team_id, conf, conf_only)` | `pointdist` | Percentage of points from FTs, 2s, and 3s. |
| `get_height(year, team_id, conf)` | `height` | Team height, experience, bench, and continuity. |
| `get_misc_stats(year, team_id, conf, conf_only)` | `misc-stats` | Miscellaneous advanced stats (shooting %, block %, steal rate, etc.). |
| `get_fanmatch(date)` | `fanmatch` | Game predictions for a given date (`YYYY-MM-DD`). |
| `get_conference_ratings(year, conf)` | `conf-ratings` | Conference efficiency ratings. |
| `get_teams(year, conf)` | `teams` | Team list with conference, coach, and arena info. |
| `get_conferences(year)` | `conferences` | Conference list with short and long names. |

## Authentication

A KenPom API subscription is required. If subscribed, your bearer token is available at
[https://kenpom.com/api-documentation.php](https://kenpom.com/account.php). You can find API documentation at [https://kenpom.com/api-documentation.php](https://kenpom.com/api-documentation.php).

## Development

```bash
# Install pre-commit hooks
pre-commit install

# Install all dependencies (including dev)
uv sync --extra dev

# Run tests
uv run pytest

# Run formatting
uv run ruff format

# Run linting
uv run ruff check
```
