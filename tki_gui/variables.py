"""Special variables that can fire events on set."""
from typing import Any, List, Callable


class Variable:
    def __init__(self):
        self._value: Any = None
        self._event_callbacks: List[Callable[[Any], None]] = []

    def _fire_set_event(self):
        for callback in self._event_callbacks:
            callback(self._value)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> Any:
        self._value = value
        self._fire_set_event()

    def add_event_callback(self, callback: Callable[[Any], None]) -> None:
        self._event_callbacks.append(callback)
    