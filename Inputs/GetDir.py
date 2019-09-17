import os

def GetDir():
        cwd = os.getcwd()
        print(("Directory: {0}".format(cwd)))
        if 'tmp/' in cwd:
           # on cx1
           datadir = '/work/lm2612/data/AvgData/'
        elif ('cx1' in cwd) or ('/export' in cwd) or ('rds' in cwd):
           # on cx1
           datadir = '/work/lm2612/data/AvgData/'
        elif ( '/home/d01/laman' in cwd ) or ('/scratch/jtmp/'in cwd ):
           # on Monsoon
           datadir = '/projects/ukca-imp/laman/AllFiles/AvgData/'
        elif '/Users/lm2612/Documents/' in cwd:
           # On Laura's Mac
           datadir = '/Users/lm2612/Documents/PhD/data/AvgData/'
        else:
            print('Not on Monsoon or on Lauras Mac- define directories to read/writeto')
            exit()
        return(datadir)
