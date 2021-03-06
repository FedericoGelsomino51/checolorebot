from pony.orm import Database, Required, Optional, Set, Json
from pony.orm import db_session, select

db = Database("sqlite", "../checolorebot.db", create_db=True)


class Regione(db.Entity):
    name = Required(str)
    color = Required(str, default="n/a")
    updatedTime = Optional(str, default="mai")
    users = Set("User")


class User(db.Entity):
    chatId = Required(int, sql_type='BIGINT', size=64)
    status = Required(str, default="selecting_region")
    wantsNotifications = Required(bool, default=True)
    dailyUpdatesTime = Required(str, default="8:00")
    region = Optional(Regione)


class Info(db.Entity):
    data = Required(Json)


# Create database
db.generate_mapping(create_tables=True)

# Create regions
with db_session:
    from modules.helpers import regionList, rules
    dbRegions = select(r.name for r in Regione)[:]
    for reg in set(regionList) - set(dbRegions):
        Regione(name=reg)
    if not Info.exists(lambda i: i.id == 1):
        Info(data=rules)
