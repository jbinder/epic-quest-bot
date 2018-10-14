from datetime import datetime

from pony.orm import Required, Optional

from common.utils.db_tools import get_database, init_database

db = get_database()


class Quest(db.Entity):
    chat_id = Required(int)
    created_by = Required(int)
    created_at = Required(datetime)
    title = Required(str)
    done_by = Optional(int)
    done_at = Optional(datetime)


init_database(db)
