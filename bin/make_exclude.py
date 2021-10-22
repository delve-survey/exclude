#!/usr/bin/env python
"""
Convert exclude files to single expnum,ccdnum list.

> python bin/make_exclude.py y*/*.txt -o delve_exclude_YYYYMMDD.fits
"""
__author__ = "Alex Drlica-Wagner"

import numpy as np
import pandas as pd
import fitsio

CCDNUMS = np.arange(1,63)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames',nargs='+')
    parser.add_argument('-o','--outfile',default='exclude.csv')
    args = parser.parse_args()

    expnum,ccdnum,reason = [],[],[]
    for f in args.filenames:
        print("Reading %s..."%f)

        if 'problem' in f:
            # 'problem' files list expnum only
            df = pd.read_csv(f,sep=r'\s{2,}',engine='python')
            d = df.to_records(index=False)
            expnum.append(np.repeat(d['Exposure'],62))
            ccdnum.append(np.tile(CCDNUMS,len(d['Exposure'])))
            reason.append(np.repeat(d['Problem'],62))
        else:
            # other files list expnum,ccdnum
            df = pd.read_csv(f,delim_whitespace=True)
            d = df.to_records(index=False)
            expnum.append(d['expnum'])
            ccdnum.append(d['ccdnum'])
            if 'ghost-scatter' in f:
                reason.append(len(d)*['Ghost/Scatter'])     
            elif 'streak' in f:
                reason.append(len(d)*['Streak'])
            elif 'noise' in f:
                reason.append(len(d)*['Noise'])
            elif 'readout' in f:
                reason.append(len(d)*['Readout'])
            else:
                reason.append(len(d)*['Unknown'])

    df = pd.DataFrame({
        'EXPNUM': np.concatenate(expnum).astype(int),
        'CCDNUM': np.concatenate(ccdnum).astype(int),
        'REASON': np.concatenate(reason)
    })
    df['ANALYST'] = 'kadrlica'
    print("Excluding %s CCDs..."%len(df))
    
    print("Writing %s..."%args.outfile)
    if args.outfile.endswith('.csv'):
        df.to_csv(args.outfile,index=False)
    elif args.outfile.endswith(('.fits','.fz')):
        fitsio.write(args.outfile,df.to_records(index=False),
                     clobber=True)
    else:
        print("Unrecognized file extension: %s"%args.outfile)

    print("Done.")
