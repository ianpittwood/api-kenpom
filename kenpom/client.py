"""KenPom API client."""

from typing import Optional

import requests


BASE_URL = "https://kenpom.com/api.php"


class KenpomClient:
    """Python wrapper for the kenpom.com API.

    Args:
        bearer_token: KenPom API bearer token obtained from a KenPom API
            subscription.
    """

    def __init__(self, bearer_token: str) -> None:
        self._bearer_token = bearer_token
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._bearer_token}",
                "Accept": "application/json",
            }
        )

    def _get(self, endpoint: str, params: Optional[dict] = None) -> list | dict:
        """Make a GET request to the KenPom API.

        Args:
            endpoint: The API endpoint name.
            params: Optional additional query parameters.

        Returns:
            The decoded JSON response body.

        Raises:
            requests.HTTPError: If the response contains an HTTP error status.
        """
        request_params: dict = {"endpoint": endpoint}
        if params:
            request_params.update({k: v for k, v in params.items() if v is not None})

        response = self._session.get(BASE_URL, params=request_params)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Ratings
    # ------------------------------------------------------------------

    def get_ratings(
        self,
        year: Optional[int] = None,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve team efficiency ratings.

        Args:
            year: Season ending year (e.g. ``2025`` for the 2024-25 season).
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``ratings`` endpoint.
        """
        return self._get("ratings", {"y": year, "team_id": team_id, "c": conf})

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------

    def get_ratings_archive_by_date(
        self,
        date: str,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve archived ratings as of a specific date.

        Args:
            date: Date in ``YYYY-MM-DD`` format.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``archive`` endpoint.
        """
        return self._get("archive", {"d": date, "team_id": team_id, "c": conf})

    def get_preseason_ratings_archive(
        self,
        year: int,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve preseason archived ratings for a given year.

        Args:
            year: Season ending year.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``archive`` endpoint.
        """
        return self._get(
            "archive",
            {"y": year, "preseason": True, "team_id": team_id, "c": conf},
        )

    # ------------------------------------------------------------------
    # Four Factors
    # ------------------------------------------------------------------

    def get_four_factors(
        self,
        year: Optional[int] = None,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
        conf_only: Optional[bool] = None,
    ) -> list | dict:
        """Retrieve four factors statistics.

        Args:
            year: Season ending year.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.
            conf_only: When ``True``, include only conference games.

        Returns:
            The decoded JSON response from the ``four-factors`` endpoint.
        """
        return self._get(
            "four-factors",
            {"y": year, "team_id": team_id, "c": conf, "conf_only": conf_only},
        )

    # ------------------------------------------------------------------
    # Point Distribution
    # ------------------------------------------------------------------

    def get_point_distribution(
        self,
        year: Optional[int] = None,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
        conf_only: Optional[bool] = None,
    ) -> list | dict:
        """Retrieve point distribution statistics.

        Args:
            year: Season ending year.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.
            conf_only: When ``True``, include only conference games.

        Returns:
            The decoded JSON response from the ``pointdist`` endpoint.
        """
        return self._get(
            "pointdist",
            {"y": year, "team_id": team_id, "c": conf, "conf_only": conf_only},
        )

    # ------------------------------------------------------------------
    # Height / Experience
    # ------------------------------------------------------------------

    def get_height(
        self,
        year: Optional[int] = None,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve team height and experience statistics.

        Args:
            year: Season ending year.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``height`` endpoint.
        """
        return self._get("height", {"y": year, "team_id": team_id, "c": conf})

    # ------------------------------------------------------------------
    # Miscellaneous Stats
    # ------------------------------------------------------------------

    def get_misc_stats(
        self,
        year: Optional[int] = None,
        team_id: Optional[int] = None,
        conf: Optional[str] = None,
        conf_only: Optional[bool] = None,
    ) -> list | dict:
        """Retrieve miscellaneous team statistics.

        Args:
            year: Season ending year.
            team_id: KenPom team ID to filter results to a single team.
            conf: Conference abbreviation to filter results.
            conf_only: When ``True``, include only conference games.

        Returns:
            The decoded JSON response from the ``misc-stats`` endpoint.
        """
        return self._get(
            "misc-stats",
            {"y": year, "team_id": team_id, "c": conf, "conf_only": conf_only},
        )

    # ------------------------------------------------------------------
    # FanMatch
    # ------------------------------------------------------------------

    def get_fanmatch(self, date: str) -> list | dict:
        """Retrieve FanMatch data for a given date.

        Args:
            date: Date in ``YYYY-MM-DD`` format.

        Returns:
            The decoded JSON response from the ``fanmatch`` endpoint.
        """
        return self._get("fanmatch", {"d": date})

    # ------------------------------------------------------------------
    # Conference Ratings
    # ------------------------------------------------------------------

    def get_conference_ratings(
        self,
        year: Optional[int] = None,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve conference efficiency ratings.

        Args:
            year: Season ending year.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``conf-ratings`` endpoint.
        """
        return self._get("conf-ratings", {"y": year, "c": conf})

    # ------------------------------------------------------------------
    # Teams
    # ------------------------------------------------------------------

    def get_teams(
        self,
        year: int,
        conf: Optional[str] = None,
    ) -> list | dict:
        """Retrieve the list of teams for a given season.

        Args:
            year: Season ending year.
            conf: Conference abbreviation to filter results.

        Returns:
            The decoded JSON response from the ``teams`` endpoint.
        """
        return self._get("teams", {"y": year, "c": conf})

    # ------------------------------------------------------------------
    # Conferences
    # ------------------------------------------------------------------

    def get_conferences(self, year: int) -> list | dict:
        """Retrieve the list of conferences for a given season.

        Args:
            year: Season ending year.

        Returns:
            The decoded JSON response from the ``conferences`` endpoint.
        """
        return self._get("conferences", {"y": year})
