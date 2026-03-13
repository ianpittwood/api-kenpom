"""Tests for KenpomClient."""

import pytest
import responses as responses_lib
from responses import matchers

from kenpom import KenpomClient

BASE_URL = "https://kenpom.com/api.php"
TOKEN = "test_bearer_token"


@pytest.fixture
def client():
    return KenpomClient(TOKEN)


@pytest.fixture(autouse=True)
def mock_responses():
    with responses_lib.RequestsMock() as rsps:
        yield rsps


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def register(rsps, endpoint: str, extra_params: dict | None = None, body=None):
    """Register a mocked GET for the given endpoint."""
    params = {"endpoint": endpoint}
    if extra_params:
        params.update(extra_params)
    if body is None:
        body = []
    rsps.add(
        responses_lib.GET,
        BASE_URL,
        match=[matchers.query_param_matcher(params)],
        json=body,
        status=200,
    )


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------


def test_client_stores_bearer_token():
    c = KenpomClient("my_token")
    assert c._bearer_token == "my_token"


def test_client_sets_auth_header(client):
    assert client._session.headers["Authorization"] == f"Bearer {TOKEN}"


# ---------------------------------------------------------------------------
# get_ratings
# ---------------------------------------------------------------------------


def test_get_ratings_no_params(mock_responses, client):
    register(mock_responses, "ratings", body=[{"TeamName": "Duke"}])
    result = client.get_ratings()
    assert result == [{"TeamName": "Duke"}]


def test_get_ratings_with_year(mock_responses, client):
    register(mock_responses, "ratings", {"y": "2025"}, body=[{"TeamName": "Kansas"}])
    result = client.get_ratings(year=2025)
    assert result == [{"TeamName": "Kansas"}]


def test_get_ratings_with_team_id(mock_responses, client):
    register(mock_responses, "ratings", {"team_id": "42"}, body=[{"TeamName": "Duke"}])
    result = client.get_ratings(team_id=42)
    assert result == [{"TeamName": "Duke"}]


def test_get_ratings_with_conf(mock_responses, client):
    register(mock_responses, "ratings", {"c": "ACC"}, body=[{"TeamName": "Duke"}])
    result = client.get_ratings(conf="ACC")
    assert result == [{"TeamName": "Duke"}]


# ---------------------------------------------------------------------------
# get_ratings_archive_by_date
# ---------------------------------------------------------------------------


def test_get_ratings_archive_by_date(mock_responses, client):
    register(mock_responses, "archive", {"d": "2024-01-15"}, body=[{"TeamName": "UNC"}])
    result = client.get_ratings_archive_by_date(date="2024-01-15")
    assert result == [{"TeamName": "UNC"}]


# ---------------------------------------------------------------------------
# get_preseason_ratings_archive
# ---------------------------------------------------------------------------


def test_get_preseason_ratings_archive(mock_responses, client):
    register(
        mock_responses,
        "archive",
        {"y": "2025", "preseason": "True"},
        body=[{"TeamName": "Gonzaga"}],
    )
    result = client.get_preseason_ratings_archive(year=2025)
    assert result == [{"TeamName": "Gonzaga"}]


# ---------------------------------------------------------------------------
# get_four_factors
# ---------------------------------------------------------------------------


def test_get_four_factors_no_params(mock_responses, client):
    register(mock_responses, "four-factors", body=[{"TeamName": "Duke"}])
    result = client.get_four_factors()
    assert result == [{"TeamName": "Duke"}]


def test_get_four_factors_conf_only(mock_responses, client):
    register(
        mock_responses,
        "four-factors",
        {"y": "2025", "conf_only": "True"},
        body=[{"TeamName": "Duke"}],
    )
    result = client.get_four_factors(year=2025, conf_only=True)
    assert result == [{"TeamName": "Duke"}]


# ---------------------------------------------------------------------------
# get_point_distribution
# ---------------------------------------------------------------------------


def test_get_point_distribution(mock_responses, client):
    register(mock_responses, "pointdist", {"y": "2025"}, body=[{"TeamName": "Auburn"}])
    result = client.get_point_distribution(year=2025)
    assert result == [{"TeamName": "Auburn"}]


# ---------------------------------------------------------------------------
# get_height
# ---------------------------------------------------------------------------


def test_get_height(mock_responses, client):
    register(mock_responses, "height", {"y": "2025"}, body=[{"TeamName": "Auburn"}])
    result = client.get_height(year=2025)
    assert result == [{"TeamName": "Auburn"}]


# ---------------------------------------------------------------------------
# get_misc_stats
# ---------------------------------------------------------------------------


def test_get_misc_stats(mock_responses, client):
    register(mock_responses, "misc-stats", {"y": "2025"}, body=[{"TeamName": "Iowa"}])
    result = client.get_misc_stats(year=2025)
    assert result == [{"TeamName": "Iowa"}]


def test_get_misc_stats_conf_only(mock_responses, client):
    register(
        mock_responses,
        "misc-stats",
        {"c": "Big Ten", "conf_only": "True"},
        body=[{"TeamName": "Iowa"}],
    )
    result = client.get_misc_stats(conf="Big Ten", conf_only=True)
    assert result == [{"TeamName": "Iowa"}]


# ---------------------------------------------------------------------------
# get_fanmatch
# ---------------------------------------------------------------------------


def test_get_fanmatch(mock_responses, client):
    register(
        mock_responses,
        "fanmatch",
        {"d": "2025-03-01"},
        body=[{"HomeTeam": "Duke", "AwayTeam": "UNC"}],
    )
    result = client.get_fanmatch(date="2025-03-01")
    assert result == [{"HomeTeam": "Duke", "AwayTeam": "UNC"}]


# ---------------------------------------------------------------------------
# get_conference_ratings
# ---------------------------------------------------------------------------


def test_get_conference_ratings(mock_responses, client):
    register(mock_responses, "conf-ratings", {"y": "2025"}, body=[{"ConfName": "ACC"}])
    result = client.get_conference_ratings(year=2025)
    assert result == [{"ConfName": "ACC"}]


def test_get_conference_ratings_with_conf(mock_responses, client):
    register(
        mock_responses,
        "conf-ratings",
        {"y": "2025", "c": "ACC"},
        body=[{"ConfName": "ACC"}],
    )
    result = client.get_conference_ratings(year=2025, conf="ACC")
    assert result == [{"ConfName": "ACC"}]


# ---------------------------------------------------------------------------
# get_teams
# ---------------------------------------------------------------------------


def test_get_teams(mock_responses, client):
    register(mock_responses, "teams", {"y": "2025"}, body=[{"TeamName": "Duke"}])
    result = client.get_teams(year=2025)
    assert result == [{"TeamName": "Duke"}]


def test_get_teams_with_conf(mock_responses, client):
    register(
        mock_responses,
        "teams",
        {"y": "2025", "c": "ACC"},
        body=[{"TeamName": "Duke"}],
    )
    result = client.get_teams(year=2025, conf="ACC")
    assert result == [{"TeamName": "Duke"}]


# ---------------------------------------------------------------------------
# get_conferences
# ---------------------------------------------------------------------------


def test_get_conferences(mock_responses, client):
    register(mock_responses, "conferences", {"y": "2025"}, body=[{"ConfName": "ACC"}])
    result = client.get_conferences(year=2025)
    assert result == [{"ConfName": "ACC"}]


# ---------------------------------------------------------------------------
# HTTP error propagation
# ---------------------------------------------------------------------------


def test_http_error_is_raised(mock_responses, client):
    mock_responses.add(
        responses_lib.GET,
        BASE_URL,
        status=401,
        json={"error": "Unauthorized"},
    )
    with pytest.raises(Exception):
        client.get_ratings()
