from ConfigParser import SafeConfigParser
from collections import OrderedDict
import os
import os.path
from sqlalchemy import create_engine

PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(PATH, "config.ini")
LOG_PATH = os.path.join(PATH, "angelzzz.log")

debug = 'DEBUG' in os.environ and os.environ['DEBUG'] == "on"

def avg(l):
    return sum(l) / float(len(l))

def iniToDict(path):
    ''' Read an ini path in to a dict
    :param path: Path to file
    :return: an OrderedDict of that path ini data
    '''
    config = SafeConfigParser()
    config.read(path)
    returnValue=OrderedDict()
    for section in reversed(config.sections()):
        returnValue[section]=OrderedDict()
        sectionTurples = config.items(section)
        for itemTurple in reversed(sectionTurples):
            returnValue[section][itemTurple[0]] = itemTurple[1]
    return returnValue

settings = iniToDict(CONFIG_PATH)
DB_PATH = "mysql+mysqlconnector://" + settings["db"]["user"] +":" + settings["db"]["password"] + "@" + settings["db"]["host"] +"/" + settings["db"]["db_name"]

def mysql_init_db():
    mysql_engine = create_engine('mysql://{0}:{1}@{2}'.format(settings["db"]["user"], settings["db"]["password"], settings["db"]["host"]))
    mysql_engine.execute("CREATE DATABASE IF NOT EXISTS {0} ".format(settings["db"]["db_name"]))
    return

def dictToIni(d, ini_path):
    
    config = SafeConfigParser()
    
    for section in d.keys():
        config.add_section(section)
        for item in d[section]:
            value = d[section][item]
            if type(value) == list:
                value = json.dumps(value)
            config.set(section,item,value)
    config.write(open(path, "w"))


def init_log():
   if os.path.isfile(LOG_PATH):
       os.remove(LOG_PATH)
    

def log(message):
    if debug:
        print(message)
    with open(LOG_PATH, 'a') as f:
        f.write(str(message.encode()) + "\n")
        f.flush()
    
