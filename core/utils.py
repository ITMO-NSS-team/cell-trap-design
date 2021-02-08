from pathlib import Path
from typing import Callable

from core.structure.domain import Domain


class GlobalEnv:
    # description of domain for optimisation
    domain: Domain = None
    # function to evaluate the model of environment
    model_func: Callable
    # link to COMSOL client (if necessary)
    comsol_client = None
    # save both fitness values and evaluated models
    full_save_load = False


def project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent
