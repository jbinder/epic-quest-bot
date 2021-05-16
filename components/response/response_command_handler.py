from common.command_handler_base import CommandHandlerBase
from common.decorators.show_typing import show_typing
from components.response.response_service import ResponseService


class ResponseCommandHandler(CommandHandlerBase):
    response_service: ResponseService

    def __init__(self, admin_id, texts, telegram_service, response_service):
        super().__init__(admin_id, texts, telegram_service)
        self.response_service = response_service

    @show_typing
    def new_message(self, bot, update):
        update.message.reply_text(self.response_service.get_random_message())
