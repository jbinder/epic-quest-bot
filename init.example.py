import os

from common.utils.logging_tools import get_logger
from components.announce.announce_command_handler import AnnounceCommandHandler
from components.announce.announce_component import AnnounceComponent
from components.core.core_command_handler import CoreCommandHandler
from components.core.core_component import CoreComponent
from components.core.texts import texts as core_texts
from components.response.response_command_handler import ResponseCommandHandler
from components.response.response_component import ResponseComponent
from components.response.response_service import ResponseService
from components.user.texts import texts as user_texts
from components.feedback.texts import texts as feedback_texts
from components.announce.texts import texts as announce_texts
from components.feedback.feedback_command_handler import FeedbackCommandHandler
from components.feedback.feedback_component import FeedbackComponent
from components.feedback.feedback_service import FeedbackService
from components.user.user_command_handler import UserCommandHandler
from components.user.user_component import UserComponent
from common.common_bot import CommonBot
from common.services.telegram_service import TelegramService
from components.user.user_service import UserService
from texts import bot_name


def create_bot(admin_id: int):
    user_service = UserService()
    telegram_service = TelegramService(user_service)
    core_command_handler = CoreCommandHandler(admin_id, core_texts, telegram_service)
    user_command_handler = UserCommandHandler(admin_id, user_texts, telegram_service, bot_name, user_service)
    feedback_service = FeedbackService()
    feedback_command_handler = FeedbackCommandHandler(admin_id, feedback_texts, telegram_service, feedback_service)
    announce_command_handler = AnnounceCommandHandler(admin_id, announce_texts, telegram_service, user_service)
    response_service = ResponseService()
    # use the test messages from the component directory
    response_service.init(ResponseService.get_absolute_file_name(os.path.join("tests", "messages.txt")))
    response_handler = ResponseCommandHandler(admin_id, {}, telegram_service, response_service)
    components = {
        # put your custom components at the top to be able to overwrite commands
        'response': ResponseComponent(response_handler),
        'feedback': FeedbackComponent(feedback_command_handler),
        'user': UserComponent(user_command_handler),
        'announce': AnnounceComponent(announce_command_handler),
        'core': CoreComponent(core_command_handler),
    }
    bot = CommonBot(components, get_logger())
    return bot
