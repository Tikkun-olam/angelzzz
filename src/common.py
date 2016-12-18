from ConfigParser import SafeConfigParser
from collections import OrderedDict
import os
import os.path

PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = "sqlite:///" + os.path.join(PATH, "angelzzz.sql")
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
    
