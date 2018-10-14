from telegram.ext import Dispatcher

from common.component_base import ComponentBase
from common.event_type import EventType
from components.quest import consts
from components.quest.quest_command_handler import QuestCommandHandler


class QuestComponent(ComponentBase):

    command_handler: QuestCommandHandler

    def __init__(self, command_handler: QuestCommandHandler):
        super().__init__()
        self.command_handler = command_handler

    def init(self, dp: Dispatcher):
        cmd_handlers = [
            (consts.cmd_quest, self.command_handler.add_quest, False),
            (consts.cmd_quests, self.command_handler.show_quests, False),
        ]
        super()._register_command_handlers(dp, cmd_handlers)

    def register_observer(self, event_type: EventType, observer: callable):
        raise NotImplementedError()
