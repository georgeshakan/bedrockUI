""" 
Typical Memory Example

[
{"role": "user", "content": "Hello, how are you?"},
{"role": "assistant", "content": "I am fine, thank you."}
]
"""

type message_history = list[dict[str, str]]


class Memory:
    """
    Class for managagment of current chat history
    """

    def __init__(self):
        self.memory = []

    def add(self, role: str, content: str) -> message_history:
        payload = {"role": role, "content": content}
        self.memory.append(payload)
        return self.memory

    def clear(self) -> message_history:
        self.memory = []
        return self.memory

    def get(self) -> message_history:
        return self.memory

    def reset(self, messages) -> message_history:
        self.memory = messages
        return self.memory

    def get_chat_id(self) -> str:
        if len(self.memory) == 0:
            raise ValueError("No chat history")
        else:
            return self.memory[0]["content"][:15]
