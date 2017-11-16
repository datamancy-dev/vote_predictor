import re
import pickle
from collections import defaultdict
import subprocess as sp
import resource_paths as rp
import pandas as pd

def separate_by_congress(votefp):
    congresses = [str(num) for num in xrange(109,116)]
    links_list = defaultdict(list)

    for congress in congresses:
        congfind = re.compile(congress)
        for path in votefp:
            if congfind.search(path) is not None:
                links_list[congress].append(path)

    return links_list

if __name__ == '__main__':
    
