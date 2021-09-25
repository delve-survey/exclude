#!/usr/bin/env python
"""
Generic python script.
"""
__author__ = "Alex Drlica-Wagner"
import glob

import os
import glob
from astropy.io import fits 
import numpy as np
import pandas as pd

INDEX = """
<html>
  <head>
    <title>Ghost/Scattered Light</title>
</head>
<body>
%(table)s
</body>
</html>
"""

TABLE = """
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>Exposure Info</th>
      <th>Camera Layout</th>
    </tr>
  </thead>
  <tbody>
%(rows)s
  </tbody>
"""

ROW = """
    <tr>
      <th>%(idx)s</th>
      <td>
        <h4>expnum: %(expnum)s</h4>
        <h4>filter: %(band)s</h4>
        <h4>run: %(run)s</h4>
      </td>
      <td> <a id="%(expnum)s"></a><a href="%(png)s"><img src="%(png)s" alt="Ghost/Scattered" width="600"></a></td>
    </tr>  
"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()

    dirname = './pngs'

    tablerows = []
    filenames = sorted(glob.glob(dirname+'/*.png'))
    for idx,filename in enumerate(filenames):
        basename = os.path.basename(filename)
        expnum = int(basename[1:9])
        band = basename[10:11]
        run = basename[12:20]
        params = dict(png=filename, expnum=expnum, band=band, idx=idx, run=run)
        tablerows.append(ROW%params)

    table = TABLE%dict(rows='\n'.join(tablerows))
    index = INDEX%dict(table=table)

    outfile = 'index.html'
    with open(outfile,'w') as out:
        out.write(index)
