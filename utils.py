"""
StadiumIQ — Shared Utilities
Reusable helpers used across route modules.
"""

import json
import logging
import os
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "static", "data")


def load_json(filename: str, default: Any = None) -> Union[List, Dict]:
    """Load and parse a JSON data file from the static/data directory.

    Args:
        filename: Name of the JSON file to load (e.g. ``stadiums.json``).
        default: Value returned when the file cannot be loaded.
                 Defaults to an empty list.

    Returns:
        Parsed JSON data, or *default* if loading fails.
    """
    if default is None:
        default = []
    try:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Data file not found: %s", filename)
        return default
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file: %s", filename)
        return default
