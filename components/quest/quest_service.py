from datetime import datetime

from pony.orm import db_session, commit, select

from common.decorators.db_use_utf8mb import db_use_utf8mb
from common.decorators.retry_on_error import retry_on_error
from components.quest.models import Quest


class QuestService:
    @db_session
    @db_use_utf8mb
    @retry_on_error
    def add(self, data):
        Quest(
            created_by=data['created_by'],
            chat_id=data['chat_id'],
            title=data['title'],
            created_at=datetime.utcnow(),
        )
        commit()

    @db_session
    @db_use_utf8mb
    @retry_on_error
    def get_all(self, chat_id):
        # noinspection PyTypeChecker
        return select(quest for quest in Quest if quest.chat_id == chat_id).order_by(lambda t: t.created_at)[:]

    @db_session
    @db_use_utf8mb
    @retry_on_error
    def complete(self, quest_id, user_id):
        # noinspection PyTypeChecker
        """ :returns True if completed, False if has been completed already """
        if Quest[quest_id].done_at is None:
            Quest[quest_id].done_at = datetime.utcnow()
            Quest[quest_id].done_by = user_id
            commit()
            return True
        return False
