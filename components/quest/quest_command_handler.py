import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from common.command_handler_base import CommandHandlerBase
from common.decorators.show_typing import show_typing
from components.quest import consts
from components.quest.quest_service import QuestService
from components.user.user_service import UserService


class QuestCommandHandler(CommandHandlerBase):
    bot_name: str
    user_service: UserService
    quest_service: QuestService

    def __init__(self, admin_id, texts, telegram_service, bot_name, user_service, quest_service):
        super().__init__(admin_id, texts, telegram_service)
        self.bot_name = bot_name
        self.quest_service = quest_service
        self.user_service = user_service

    @show_typing
    def add_quest(self, bot, update):
        text = update.message.text[(len(consts.cmd_quest) + 1):].strip()
        if text == f"@{self.bot_name}" or not text:
            update.message.reply_text(self.texts['missing-title'](update.effective_user.first_name))
            return

        data = {'title': text, 'created_by': update.effective_user.id, 'chat_id': update.effective_chat.id}
        self.quest_service.add(data)

        update.message.reply_text(self.texts['quest-added'], quote=True)

    @show_typing
    def show_quests(self, bot, update):
        quests = self.quest_service.get_all(update.effective_chat.id)
        open_quests = [quest.title for quest in quests if quest.done_at is None]
        done_quests = [quest.title for quest in quests if quest.done_at is not None]
        open_quests_txt = "\n".join(open_quests) if len(open_quests) >= 1 else "-"
        done_quests_txt = "\n".join(done_quests) if len(done_quests) >= 1 else "-"
        message = f"{self.texts['quests-open']}\n{open_quests_txt}\n\n" + \
                  f"{self.texts['quests-done']}\n{done_quests_txt}"
        update.message.reply_text(message, quote=False)

    @show_typing
    def complete_quest(self, bot, update):
        quests = self.quest_service.get_all(update.effective_chat.id)
        open_quests = [quest for quest in quests if quest.done_at is None]
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=quest.title, callback_data=f"quest_id:{quest.id}:{quest.title}")]
             for quest in open_quests])
        update.message.reply_text(self.texts['select-quest-to-complete'], reply_markup=markup, quote=False)

    def inline_handler(self, bot, update):
        data = re.split("[:,\n]", update.callback_query.data)
        if data[0] == "quest_id":
            self.telegram_service.remove_inline_keybaord(bot, update.callback_query)
            quest_id = int(data[1])
            quest_title = data[2]
            user_id = update.effective_user.id
            if self.quest_service.complete(quest_id, user_id):
                bot.send_message(update.effective_chat.id, self.texts['quest-completed'](quest_title))
            else:
                bot.send_message(update.effective_chat.id, self.texts['quest-complete-error'](quest_title))
        else:
            raise ValueError()
