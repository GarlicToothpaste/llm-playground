from query_data import query_rag
from ollama import generate

#To Run: pytest -s

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match value of the expected response, disregard symbols? 
"""

def test_monopoly_rules():
    assert query_and_validate(
        question="How much total money does a player start with in Monopoly? (Answer with the number only)",
        expected_response="$1500",
    )

def test_snakes_and_ladders_rules():
    assert query_and_validate(
        question="What square do you need to reach to win snakes and ladders (Answer with the number only)",
        expected_response="100",
    )

def query_and_validate(question: str , expected_response : str):
    response_text = query_rag(question)
    print(response_text)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )
    response = generate(model='mistral-small:24b', prompt=prompt)
    response = response.response.strip().lower()
    print (prompt)
    print(response)

    # response=response.response
    if "true" in response:
        print(response)
        return True
    elif "false" in response:
        print(response)
        return False
    else:
        raise ValueError("Invalid Result")

# query_and_validate("How much total money does a player start with in Monopoly? (Answer with the number only)", "$1500")