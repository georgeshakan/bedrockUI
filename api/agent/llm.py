from xmlrpc.client import boolean
import boto3
import json
import os
from dotenv import load_dotenv
from .memory import Memory
from .utils import get_base64_of_image
from .storage import Database
from typing import Generator

type message_history = list[dict[str, str]]


class LLM:
    def __init__(self, modelId: str):
        """
        modelId: AWS Bedrock model id
                 such as anthropic.claude-3-sonnet-20240229-v1:0
        """
        load_dotenv()
        profile_name = os.environ.get("AWS_PROFILE", "")
        self.session = boto3.Session(profile_name=profile_name)
        self.client = self.session.client("bedrock-runtime")
        self.modelId = modelId
        self.memory = Memory()
        self.db = Database()

    def query(
        self, message: str, image: None | str = None, stream=None
    ) -> str | Generator[str, None, None]:

        if image:
            encoded_string = get_base64_of_image(image)
            payload = [
                {"type": "text", "text": message},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": encoded_string,
                    },
                },
            ]
        self.memory.add("user", message)

        response = self.get_response(self.memory.get())
        if stream:
            return self.streamer(response)
        content = ""
        for x in response["body"]:
            try:
                c = json.loads(x["chunk"]["bytes"].decode())["delta"]["text"]
                content += c
            except:
                pass
        self.memory.add("assistant", content)

        return content

    def process_agent_message(self, content: str) -> None:
        self.memory.add("assistant", content)
        chatId = self.memory.get_chat_id()
        self.db.put(chatId, self.memory.get())
        return

    def new_memory(self, chatId: str) -> None:
        self.memory.clear()
        self.memory.reset(self.db.get(chatId))
        return

    def get_response(self, messages: message_history) -> dict:

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": messages,
        }

        response = self.client.invoke_model_with_response_stream(
            body=json.dumps(payload), modelId=self.modelId
        )

        return response

    def streamer(self, response: dict) -> Generator[str, None, None]:
        if response:
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code != 200:
                raise ValueError(f"Error invoking Bedrock API: {status_code}")
            for response in response["body"]:
                json_response = json.loads(response["chunk"]["bytes"])

                yield json_response.get("delta", {}).get("text", "")
