import json

from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage

class MessagesEncoder(json.JSONEncoder):
    """Encoder for messages to JSON."""

    def default(self, o):
        """
        Encode a message to JSON based on the object type.

        Args:
        - o: Object to encode.

        Returns:
        - dict: Dictionary representation of the object for JSON encoding.
        """
        if isinstance(o, HumanMessage):
            return {"type": "human", "content": o.content}
        elif isinstance(o, AIMessage):
            return {"type": "ai", "content": o.content}
        else:
            return super().default(o)


class MessagesDecoder(json.JSONDecoder):
    """Decoder for messages from JSON."""

    def __init__(self):
        """
        Initialize the JSONDecoder with a custom object hook.

        Sets the object_hook to self.decode_message for decoding JSON objects.

        Args:
        - self: Instance of the MessagesDecoder class.
        """
        json.JSONDecoder.__init__(self, object_hook=self.decode_message)

    def decode_message(self, obj):
        """
        Decode a message from a JSON object.

        Args:
        - obj: JSON object to decode.

        Returns:
        - Object: Decoded object based on 'type' and 'content' fields.
        """
        if "type" in obj and "content" in obj:
            if obj["type"] == "human":
                return HumanMessage(content=obj["content"])
            elif obj["type"] == "ai":
                return AIMessage(content=obj["content"])
        return obj
