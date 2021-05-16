from telegram.ext import Dispatcher, Filters

from common.component_base import ComponentBase
from common.event_type import EventType
from components.response.response_command_handler import ResponseCommandHandler


class ResponseComponent(ComponentBase):

    command_handler: ResponseCommandHandler

    def __init__(self, command_handler: ResponseCommandHandler):
        super().__init__()
        self.command_handler = command_handler

    def init(self, dp: Dispatcher):
        msg_handlers = [
            (Filters.text, self.command_handler.new_message)
        ]
        super()._register_message_handlers(dp, msg_handlers)


    def register_observer(self, event_type: EventType, observer: callable):
        raise NotImplementedError()
