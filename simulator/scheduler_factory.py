from typing import Type
from .base_scheduler import BaseScheduler
from .scheduler import RoundRobinScheduler
from .proportional_fair_scheduler import ProportionalFairScheduler

class SchedulerFactory:
    """
    Factory class to create scheduler objects based on a string identifier.
    Supported schedulers: 'round_robin', 'proportional_fair'.
    Returns objects implementing the BaseScheduler interface.
    """
    _schedulers = {
        "round_robin": RoundRobinScheduler,
        "proportional_fair": ProportionalFairScheduler,
    }

    @staticmethod
    def create(scheduler_type: str) -> BaseScheduler:
        """
        Create a scheduler object based on the given identifier.
        Args:
            scheduler_type (str): The type of scheduler ('round_robin', 'proportional_fair').
        Returns:
            BaseScheduler: An instance of the requested scheduler.
        Raises:
            ValueError: If the scheduler_type is not supported.
        """
        scheduler_type = scheduler_type.lower()
        if scheduler_type not in SchedulerFactory._schedulers:
            raise ValueError(f"Unsupported scheduler type: {scheduler_type}")
        return SchedulerFactory._schedulers[scheduler_type]()
