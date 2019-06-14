import os
import peewee
from peewee import *

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
database = peewee.SqliteDatabase(PATH("data.sqlite"))

class BaseModel(Model):
    class Meta:
        database = database
		
class system_disk_monitor(BaseModel):
    size=CharField()
    used=CharField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'system_disk_monitor'

class system_uptime(BaseModel):
    average=CharField()
    user=CharField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'system_uptime'
