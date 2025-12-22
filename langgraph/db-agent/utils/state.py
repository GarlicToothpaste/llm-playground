from typing_extensions import TypedDict, Literal

class OperationClassification(TypedDict):
    operation : Literal['show_items','add_item', 'update_item']

class AgentState(TypedDict):
    message_content : str
    operation : OperationClassification | None
    item_name : str | None 
    description : str | None
    quantity : int | None