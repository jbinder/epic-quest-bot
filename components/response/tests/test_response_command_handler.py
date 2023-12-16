import os
import time
from unittest import mock

from telegram.ext import MessageHandler, Filters

from common.services.telegram_service import TelegramService
from common.test.PtbTestCase import PtbTestCase
from components.response.response_command_handler import ResponseCommandHandler
from components.user.user_service import UserService


class TestFeedbackCommandHandler(PtbTestCase):

    @mock.patch.dict(os.environ, {'DFM_ENV': 'Test'})
    def setUp(self):
        PtbTestCase.setUp(self)
        from components.response.response_service import ResponseService
        self.service = ResponseService()
        self.service.init(ResponseService.get_absolute_file_name(os.path.join("tests", "messages.txt")))
        self.handler = ResponseCommandHandler(-1, {}, TelegramService(UserService()), self.service)

    def test_reply_to_message(self):
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.handler.new_message))
        self.updater.start_polling()
        update = self.mg.get_message(text="hi")

        self.bot.insertUpdate(update)

        time.sleep(1)  # the message takes some time to be sent...
        self.assertEqual(2, len(self.bot.sent_messages))
        sent = self.bot.sent_messages[0]
        self.assertEqual("sendChatAction", sent['method'])
        self.assertEqual("typing", sent['action'])
        sent = self.bot.sent_messages[1]
        self.assertEqual("sendMessage", sent['method'])
        self.assertTrue(len(sent['text']) > 0)
        self.updater.stop()
