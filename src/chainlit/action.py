import uuid
from typing import Optional

from dataclasses_json import DataClassJsonMixin
from pydantic.dataclasses import Field, dataclass

from chainlit.context import get_emitter
from chainlit.telemetry import trace_event


@dataclass
class Action(DataClassJsonMixin):
    # Name of the action, this should be used in the action_callback
    name: str
    # The value associated with the action. This is useful to differentiate between multiple actions with the same name.
    value: str
    # The label of the action. This is what the user will see. If not provided the name will be used.
    label: str = ""
    # The description of the action. This is what the user will see when they hover the action.
    description: str = ""
    # This should not be set manually, only used internally.
    forId: Optional[str] = None
    # The ID of the action
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        trace_event(f"init {self.__class__.__name__}")
        self.emit = get_emitter().emit

    async def send(self, for_id: str):
        trace_event(f"send {self.__class__.__name__}")
        self.forId = for_id
        await self.emit("action", self.to_dict())

    async def remove(self):
        trace_event(f"remove {self.__class__.__name__}")
        await self.emit("remove_action", self.to_dict())
