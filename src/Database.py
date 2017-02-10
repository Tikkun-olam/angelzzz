from sqlalchemy import  create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Database declaration

class AngelzzzDB(Base):
    """This is the SQLiteAlchemy database structure, in the declarative form"""
    __tablename__ = "log"
    
    time = Column(DATETIME(fsp=3), primary_key=True)
    beddit = Column(String(255))
    channel1 = Column(Float)
    channel2 = Column(Float)

    def __init__(self,time, beddit, channel1, channel2):
        self.time = time
        self.beddit = beddit
        self.channel1 = channel1
        self.channel2 = channel2
    
    #def __repr__(self):
    #    return "<AngelzzzDB(time='%f', beddit='%s', channel1='%f', channel2='%f')>" % (self.time, self.beddit, self.channel1, self.channel2)

