import os
import json

type message_history = list[dict[str, str]]


class Database:
    """
    Psuedo Data Base that uses txt files to store chat history
    """

    def __init__(self):
        pass

    def create(self, chat_id: str) -> None:
        """
        chat_id : chat id of the chat

        Creates a json file with the chat_id as the name in the history directory.

        I have implemented it to be the first 15 characters of the first message.
        Of course, this may not be unique, but it's a risk I'm willing to take.


        """
        # if file exists, raise error
        if os.path.exists(f"history/{chat_id}.json"):
            raise ValueError("Chat already exists")
        with open(f"history/{chat_id}.json", "w") as f:
            json.dump([], f)

    def delete(self, chat_id: str) -> None:
        """
        Delete the chat history file
        """
        if os.path.exists(f"history/{chat_id}.json"):
            os.remove(f"history/{chat_id}.json")

    def put(self, chat_id: str, messages: message_history) -> None:
        # if file exists, remove
        if os.path.exists(f"history/{chat_id}.json"):
            os.remove(f"history/{chat_id}.json")
        with open(f"history/{chat_id}.json", "w") as f:
            json.dump(messages, f)

    def append(self, chat_id: str, message: dict[str, str]) -> None:
        with open(f"history/{chat_id}.json", "r") as f:
            messages = json.loads(f.read())
            messages.append(message)
        with open(f"history/{chat_id}.json", "w") as f:
            json.dump(messages, f)

    def get(self, file_name: str) -> message_history:
        """
        Read the chat history file."""
        try:
            with open(f"history/{file_name}.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
