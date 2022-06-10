#!/usr/bin/env python
"""
Download exposures for each year.
"""
__author__ = "Alex Drlica-Wagner"
from collections import OrderedDict as odict
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

SISPI_QUERY = """
SELECT TO_CHAR(date-'12 hours'::INTERVAL,'YYYYMMDD')::INT AS "#nite", 
       id AS expnum, 
       telra AS ra, 
       teldec AS dec, 
       filter AS fil, 
       exptime AS exp, 
       '{'||substring(object, 0, 21)||'}' AS object,
       airmass AS secz, 
       TO_CHAR(TO_TIMESTAMP(utc_dark),'HH:MM') AS ut, 
       'good' as status
FROM exposure
WHERE 
TO_CHAR(date-'12 hours'::INTERVAL,'YYYYMMDD')::INT between %(start)s AND %(end)s
AND filter in ('g','r','i','z') and exptime >= 30
AND flavor = 'object' AND discard = False AND delivered = True
AND propid NOT IN (
    '2012B-0001', -- DES WIDE
    '2012B-0002', -- DES SN
    '2012B-0003', -- DES SV
    '2012B-0004', -- DECAM SV SN
    '2012B-9996', -- DES DC7
    '2012B-9997', -- DECam Test
    '2012B-9998', -- DECam Test
    '2012B-9999', -- Commissioning
    '2013A-9999', -- Engineering
    '2014A-9000'  -- Standards
)
AND id NOT BETWEEN 222736 AND 223265 -- quotes in object name
ORDER BY id
--LIMIT 10000
"""

DELVE_QUERY = """
SELECT e.nite AS "#nite", 
       e.expnum, 
       e.radeg AS ra, 
       e.decdeg AS dec, 
       e.band AS fil, 
       e.exptime AS exp, 
       '{'||substring(e.object, 0, 21)||'}' AS object,
       e.airmass AS secz, 
       TO_CHAR(date_obs,'HH:MM') AS ut, 
       'good' as status
FROM exposure e, qa_summary q
WHERE 
e.expnum = q.expnum
AND e.nite between %(start)s AND %(end)s
AND e.band in ('g','r','i','z') and e.exptime >= 30
AND abs(e.glat) > 9 AND e.obstype = 'object'
AND q.t_eff > 0.1 and q.psf_fwhm < 2.0
AND e.propid NOT IN (
    '2012B-0001', -- DES WIDE
    '2012B-0002', -- DES SN
    '2012B-0003', -- DES SV
    '2012B-0004', -- DECAM SV SN
    '2012B-9996', -- DES DC7
    '2012B-9997', -- DECam Test
    '2012B-9998', -- DECam Test
    '2012B-9999', -- Commissioning
    '2013A-9999', -- Engineering
    '2014A-9000'  -- Standards
)
AND e.expnum NOT BETWEEN 222736 AND 223265 -- quotes in object name
ORDER BY e.expnum
--LIMIT 10000
"""

# Note that tcl code can only accept years y1 to y9
# To add more years, we'll need to fake it...
# Scattered light ends 20140314 so y1 is a bit short and y2 is long
YEARS = odict([
    (0, [20121024,20130801]), 
    (1, [20130801,20140314]), 
    (2, [20140314,20150801]),
    (3, [20150801,20160801]),
    (4, [20160801,20170801]),
    (5, [20170801,20180801]),
    (6, [20180801,20190801]),
    (7, [20190801,20200801]),
    (8, [20200801,20210801]),
    (9, [20210801,20220801]),
])    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-y', '--year', default=None, type=int,
                        help='year to query')
    parser.add_argument('--db', default='sispi', choices=['sispi','delve'],
                        help='database for query')
    parser.add_argument('--explist', default=None,
                        help='exposure list to select from')
    args = parser.parse_args()

    if args.db.lower() in ('sispi'):
        conn = 'postgresql://decam_reader@des61.fnal.gov:5443/decam_prd'
        QUERY = SISPI_QUERY
    elif args.db.lower() in ('delve','bliss'):
        conn = 'postgresql://des_reader@des51.fnal.gov:5432/BLISS'
        QUERY = DELVE_QUERY
    else:
        msg = 'Unrecognized database: %s'%args.db
        raise Exception(msg)

    engine = create_engine(conn)

    for year,(start,end) in YEARS.items():
        if (args.year is not None) and (year != args.year): 
            continue
            
        query = QUERY%dict(start=start,end=end)
        df = pd.read_sql_query(query,con=engine)

        if args.explist:
            # Only select exposures in the explist
            explist = pd.read_csv(args.explist)
            df = df[np.in1d(df['expnum'],explist['expnum'])]

        outfile = 'survey-y{}.txt'.format(year)
        print("Writing {}...".format(outfile))
        df.to_csv(outfile,index=False,sep='\t')
