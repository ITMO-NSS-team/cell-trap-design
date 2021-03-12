from pathlib import Path
from typing import Callable

from core.structure.domain import Domain


class GlobalEnv(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalEnv, cls).__new__(cls)
        return cls.instance

    # description of domain for optimisation
    domain: Domain = None
    # function to evaluate the model of environment
    model_func: Callable
    # link to COMSOL client (if necessary)
    comsol_client = None
    # save both fitness values and evaluated models
    full_save_load = False

    # initial polygon for optimisation start
    initial_state = None


def project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent
