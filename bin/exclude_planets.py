#!/usr/bin/env python
"""
Generic python script.
"""
__author__ = "Alex Drlica-Wagner"

import numpy as np
import pylab as plt
import easyaccess as ea

conn = ea.connect('decade')

data = [
    dict(planet='saturn',nite=20190702,emin=869331,emax=869400, ccd=[44]),
    dict(planet='saturn',nite=20190702,emin=869405,emax=869474, ccd=[19, 25, 26]),
    dict(planet='saturn',nite=20190703,emin=869479,emax=869552, ccd=[44]),
    dict(planet='saturn',nite=20190703,emin=869798,emax=869868,ccd=[19, 25, 26]),
    dict(planet='saturn',nite=20190703,emin=869873,emax=869942,ccd=[44]),
    dict(planet='saturn',nite=20190704,emin=869947,emax=870011,ccd=[19, 25, 26]),
    dict(planet='jupiter',nite=20190704,emin=870170,emax=870211, ccd=[13,14,19,20,21,25,26,27,32,33,49]),
    dict(planet='saturn',nite=20190704,emin=870222,emax=870365, ccd=[38]),
    dict(planet='saturn',nite=20190704,emin=870370,emax=870422, ccd=[2, 38]),
    dict(planet='jupiter',nite=20190705,emin=870618,emax=870635, ccd=[32,33,34,39,40]),
    dict(planet='saturn',nite=20190705,emin=870644,emax=870704, ccd=[19,25,26]),
    dict(planet='saturn',nite=20190705,emin=870709,emax=870768, ccd=[44]),
    dict(planet='saturn',nite=20190705,emin=870773,emax=870847, ccd=[19,25,26]),
]

for d in data:
    print()
    print(d['nite'],d['planet'],d['emin'],d['emax'],d['ccd'])
    query = """
    select nite||'  '||expnum||' nan nan  ' as text
    from exposure 
    where obstype='object' and propid = '2019A-0915' and band in ('g','r','i','z') and exptime > 30 and 
    expnum between %(emin)s and %(emax)s
    order by expnum;    
    """%d
    print(query)

    df = conn.query_to_pandas(query)
    for i,row in df.iterrows():
        for ccd in d['ccd']:
            print(row['TEXT']+"%2d"%ccd)


