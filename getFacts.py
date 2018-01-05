import re
import json
import sys
import random
import urllib.request
import html

import basic

# get page
facts = urllib.request.urlopen("https://en.wikipedia.org/wiki/"+sys.argv[1]).read().decode('utf-8')

# get paragraphs
facts = '\n'.join(re.findall(r'<p>(.*)</p>', facts))

# remove html tags
facts = re.sub(r'<[^>]*>','', facts)

# translate html entities
facts = html.unescape(facts)

# replace newlines wih spaces
facts = ' '.join(facts.split())


# split around sentence ends
facts = re.compile("\.(?:\[[^\]]*\])* (?=[A-Z0-9])").split(facts)
facts = [fact for fact in facts if fact.strip()]
facts = [fact+'. ' for fact in facts]
random.shuffle(facts)

# recombine as lines
facts = '\n'.join(facts)

# log
print(facts)

# save new file
procfile = open(basic.folder()+"cats/catfacts",'w')
procfile.write(facts)
procfile.close()
