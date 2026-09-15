from io import StringIO

import pandas as pd
import requests


TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

EXOPLANET_QUERY = """
    SELECT
        pl_name,
        hostname,
        pl_orbper,
        pl_bmassj,
        st_met,
        st_metratio
    FROM pscomppars
    WHERE
        pl_orbper IS NOT NULL
        AND pl_bmassj IS NOT NULL
        AND st_met IS NOT NULL
"""


class ExoplanetArchiveError(RuntimeError):
    """Raised when data can't be retrieved from the NASA Exoplanet Archive."""


def fetch_exoplanets(timeout: int = 30) -> pd.DataFrame:
    """Retrieve the exoplanet sample needed for the experiment.

    Returns:
    DataFrame
        Planet name, host star, orbital period, best mass estimate,
        stellar metallicity, and metallicity ratio.

    """
    try:
        response = requests.get(
            TAP_URL,
            params={
                "query": EXOPLANET_QUERY,
                "format": "csv",
            },
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExoplanetArchiveError(
            "Could not retrieve data from the NASA Exoplanet Archive."
        ) from exc

    dataframe = pd.read_csv(StringIO(response.text))

    if dataframe.empty:
        raise ExoplanetArchiveError(
            "The NASA Exoplanet Archive returned an empty dataset."
        )

    return dataframe