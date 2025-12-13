from typing_extensions import TypedDict, Literal

class OperationClassification(TypedDict):
    platform : Literal['add_item', 'update_item']

class AgentState(TypedDict):
    message_content : str
    classification : OperationClassification | None