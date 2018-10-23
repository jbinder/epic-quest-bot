import os
import unittest
from datetime import datetime
from unittest import mock

from pony.orm import db_session, select

from components.quest.models import Quest


class TestQuestService(unittest.TestCase):

    chat_id: int
    user1_id: int
    user2_id: int
    title: str

    @mock.patch.dict(os.environ, {'DFM_ENV': 'Test'})
    def setUp(self):
        from components.quest.models import db
        from components.quest.quest_service import QuestService
        self.chat_id = 1
        self.user1_id = 1
        self.user2_id = 2
        self.title = "a quest"
        self.service = QuestService()
        db.drop_all_tables(with_all_data=True)
        db.create_tables()

    @db_session
    def test_add_valid_data(self):
        self.service.add(self._get_quest(self.chat_id))
        # noinspection PyTypeChecker
        quests = select(quest for quest in Quest)[:]
        self.assertEqual(1, len(quests))

    def test_add_invalid_data(self):
        with self.assertRaises(KeyError):
            self.service.add({})

    def test_get_all_quests_exist(self):
        self.service.add(self._get_quest(self.chat_id))
        self.service.add(self._get_quest(0))
        quests = self.service.get_all(self.chat_id)
        self.assertEqual(1, len(quests))
        self.assertEqual(self.title, quests[0].title)
        self.assertEqual(self.user1_id, quests[0].created_by)
        self.assertEqual(self.chat_id, quests[0].chat_id)
        self.assertGreater(datetime.utcnow(), quests[0].created_at)

    def test_get_all_no_quest_exists(self):
        quests = self.service.get_all(self.chat_id)
        self.assertEqual(0, len(quests))

    def test_complete_valid_quest_id(self):
        self.service.add(self._get_quest(self.chat_id))
        quest = self.service.get_all(self.chat_id)[0]
        self.service.add(self._get_quest(self.chat_id))
        result = self.service.complete(quest.id, self.user2_id)
        self.assertTrue(result)
        quests = self.service.get_all(self.chat_id)
        for actual_quest in quests:
            is_completed_quest = actual_quest.id == quest.id
            self.assertEqual(is_completed_quest, actual_quest.done_at is not None)
            self.assertEqual(is_completed_quest, actual_quest.done_by == self.user2_id)
        result = self.service.complete(quest.id, self.user2_id)
        self.assertFalse(result)

    def test_stats_quests_exist(self):
        self.service.add(self._get_quest(self.chat_id))
        self.service.add(self._get_quest(self.chat_id))
        self.service.add(self._get_quest(self.chat_id))
        quest = self.service.get_all(self.chat_id)[0]
        self.service.complete(quest.chat_id, self.user2_id)
        stats = self.service.get_stats(self.chat_id)
        self.assertEqual({'count': 3, 'done': 1}, stats)

    def test_stats_no_quests_exist(self):
        self.service.add(self._get_quest(0))
        stats = self.service.get_stats(self.chat_id)
        self.assertEqual({'count': 0, 'done': 0}, stats)

    def _get_quest(self, chat_id):
        return {'chat_id': chat_id, 'created_by': self.user1_id, 'title': self.title}


if __name__ == '__main__':
    unittest.main()
