from database.db import session
from seeders.db_seed import seed


db = session

print(seed(db=db))