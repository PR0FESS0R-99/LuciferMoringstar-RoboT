import datetime
import motor.motor_asyncio # pylint: disable=import-error
from config import DATABASE_URI, DATABASE_NAME

class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
        self.db = self._client[DATABASE_NAME]
        self.dcol = self.db.users
        
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat()
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.dcol.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.dcol.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.dcol.count_documents({})
        return count

    async def get_all_users(self):
        return self.dcol.find({})

    async def delete_user(self, user_id):
        await self.dcol.delete_many({'id': int(user_id)})


db = Database()
