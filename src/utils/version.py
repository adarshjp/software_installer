from packaging import version
from packaging.version import InvalidVersion
import logging

logger = logging.getLogger(__name__)

def is_newer_version(latest: str, current: str) -> bool:
    """
    Compares two version strings to determine if the 'latest' version is newer than the 'current' version.

    Args:
        latest: The version string considered to be the latest.
        current: The version string considered to be the current.

    Returns:
        True if 'latest' is a newer version than 'current', False otherwise.
        Returns False if either version string is invalid or cannot be parsed.
    """
    try:
        return version.parse(latest) > version.parse(current)
    except InvalidVersion as e:
        logger.warning(f"Could not parse version strings for comparison: latest='{latest}', current='{current}'. Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error comparing versions: latest='{latest}', current='{current}'. Error: {e}")
        return False
