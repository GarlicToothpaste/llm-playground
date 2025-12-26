from typing_extensions import TypedDict, Literal

class OperationClassification(TypedDict):
    operation : Literal['show_items','add_item', 'update_item']

class ItemDetails(TypedDict):
    item_name : str | None 
    old_item_name : str | None
    description : str | None
    quantity : int | None

class AgentState(TypedDict):
    message_content : str
    operation : OperationClassification | None
    item_details : ItemDetails | None