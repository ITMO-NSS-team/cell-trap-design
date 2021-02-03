from pathlib import Path
from typing import Callable

from core.structure.domain import Domain


class GlobalEnv:
    domain: Domain = None
    model_func: Callable
    comsol_client = None


def project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent
