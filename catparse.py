import re
import json
import sys
import random

import basic

rawfile = open("rawcatfacts",'r')
rawdata = rawfile.read()
rawfile.close()
rawdata = ' '.join(rawdata.split())

facts=re.compile("\.(?:\[[^\]]*\])* (?=[A-Z0-9])").split(rawdata)
facts= [fact for fact in facts if fact.strip()]
facts = [fact+'. ' for fact in facts]
random.shuffle(facts)

procfile = open(basic.folder()+"cats/catfacts",'w')
procfile.write('\n'.join(facts))
procfile.close()
