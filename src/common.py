from ConfigParser import SafeConfigParser
from collections import OrderedDict

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
    
