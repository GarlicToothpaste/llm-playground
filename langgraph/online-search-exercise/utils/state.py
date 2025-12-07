from typing_extensions import TypedDict, Literal

class MessageClassification(TypedDict):
    platform : Literal['wikipedia', 'duckduckgo']

class MessageState(TypedDict):
    message_content : str
    search_summary : str | None
    classification : MessageClassification | None
    search_result : str | None