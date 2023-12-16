import os
import random
import string


class ResponseService:

    messages: [string]

    def init(self, file_name: string):
        self.messages = self._read_messages(file_name)

    def get_random_message(self):
        return random.choice(self.messages)

    @staticmethod
    def _read_messages(file_name: string):
        with open(file_name, 'r') as f:
            messages = f.readlines()
            return messages

    @staticmethod
    def get_absolute_file_name(file_name: string):
        base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, file_name)
