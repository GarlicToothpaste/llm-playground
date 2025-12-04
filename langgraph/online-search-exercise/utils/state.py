from typing_extensions import TypedDict, Literal

class MessageState(TypedDict):
    message_content : str
    platform_search : Literal['wikipedia' , 'duckduckgo'] | None
    search_result : str | None