from langchain.chat_models import ChatOpenAI as BaseChatOpenAI
import logging

logger = logging.getLogger(__name__)

class ChatOpenAI(BaseChatOpenAI):
    def __init__(self, temperature, model_name):
        if not (0 <= temperature <= 1):
            logger.error("Invalid temperature. Must be between 0 and 1.")
            return
        if not model_name:
            logger.error("Invalid model name.")
            return
        super().__init__(temperature=temperature, model_name=model_name)
