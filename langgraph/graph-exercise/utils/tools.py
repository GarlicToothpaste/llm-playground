from langchain.tools import tool

@tool
def send_email(email: str ) -> str:
    """Given an email address, send an email.
    
    Args :
        email: Email Address of the User
    """

    status = "Email sent!"
    return status

@tool
def send_text_message(mobile_number: str) -> str:
    """Given a mobile number, send a text message

    Args:
        a: mobile number of the recipient
    """
    return mobile_number
