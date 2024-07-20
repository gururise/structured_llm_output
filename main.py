from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_together import ChatTogether
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import json
import sys

def main():
    load_dotenv()  # take environment variables from .env.

    llm = ChatTogether(model="mistralai/Mistral-7B-Instruct-v0.1")
    #llm = ChatOpenAI(model='gpt-4o-mini')

    class Joke(BaseModel):
        """Joke to tell user."""
        setup: str = Field(description="The setup of the joke")
        punchline: str = Field(description="The punchline to the joke")
        rating: Optional[int] = Field(description="How funny the joke is, from 1 to 10")

    structured_llm = llm.with_structured_output(Joke)

    # Get input from command line
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = "Tell me a joke about cats"  # Default input if no command-line argument is provided

    result = structured_llm.invoke(user_input)
    # Convert the result to a dictionary
    result_dict = result.dict()
    
    # Print the JSON output
    print(json.dumps(result_dict, indent=2))


if __name__ == "__main__":
    main()
