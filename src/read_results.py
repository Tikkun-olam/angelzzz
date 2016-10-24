from sqlalchemy import create_engine
from sqlalchemy.sql import select
from Database import AngelzzzDB, Base
from angelzzz_server import DB_PATH


if __name__ == "__main__":
    engine = create_engine(DB_PATH)
    conn = engine.connect()
    s = select([AngelzzzDB])
    result = conn.execute(s)
    count = 0
    for row in result:
        count+=1
        print(str(row["time"]) + "," + str(row["channel1"]) + "," +  str(row["channel2"]))
    #print(count)
