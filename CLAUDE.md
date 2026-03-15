# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an unofficial Python wrapper for the kenpom.com API, providing a clean interface to access college basketball statistics and ratings data. The library requires Python 3.12+ and uses `uv` for dependency management.

## Development Commands

### Setup
```bash
# Install all dependencies including dev dependencies
uv sync --extra dev

# The project uses a virtual environment at .venv/
# Dependencies are locked in uv.lock
```

### Testing
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_client.py

# Run a specific test function
uv run pytest tests/test_client.py::test_get_ratings_with_year

# Run tests with verbose output
uv run pytest -v
```

### CI/CD
The project uses GitHub Actions for CI. Tests run automatically on:
- Pushes to `main` branch
- All pull requests

## Architecture

### Core Components

**`kenpom/client.py`** - The main `KenpomClient` class that wraps all API endpoints. Architecture:
- Uses `requests.Session` for connection pooling and persistent headers
- All API methods funnel through a single `_get()` method that handles authentication and request building
- The base URL is `https://kenpom.com/api.php` with endpoints specified via query parameter `?endpoint=<name>`
- Authentication via Bearer token in Authorization header
- All methods return decoded JSON (either `list` or `dict`)

**API Parameter Mapping**: The client methods use readable Python parameter names that get mapped to KenPom's abbreviated query parameters:
- `year` → `y`
- `conf` → `c`
- `date` → `d`
- Parameters set to `None` are automatically excluded from requests

### Testing Strategy

Tests use the `responses` library to mock HTTP requests without hitting the real API. Key patterns:
- The `register()` helper function sets up mocked responses with expected query parameters
- Each endpoint has separate tests for different parameter combinations
- The `mock_responses` fixture is autouse, so all tests automatically get request mocking
- Tests verify both request parameters and response parsing

### API Endpoints

The wrapper organizes endpoints into logical groups:
1. **Ratings** - Current season efficiency ratings
2. **Archive** - Historical ratings (by date or preseason)
3. **Four Factors** - Dean Oliver's four factors of basketball success
4. **Point Distribution** - Scoring breakdowns (FT%, 2P%, 3P%)
5. **Height/Experience** - Team composition metrics
6. **Misc Stats** - Additional advanced statistics
7. **FanMatch** - Game predictions
8. **Conference Ratings** - Conference-level metrics
9. **Teams** - Team directory with metadata
10. **Conferences** - Conference directory

### Key Constraints

- A KenPom API subscription is required (bearer token from https://kenpom.com/account.php)
- Year parameters use the season ending year (e.g., 2025 for 2024-25 season)
- Date parameters must be in `YYYY-MM-DD` format
- Some endpoints require at least one of `year` or `team_id` (see `get_ratings()`)
- Boolean parameters (like `conf_only`, `preseason`) get serialized to string "True" by requests