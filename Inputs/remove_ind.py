import numpy as np
def remove_ind(Names,name_to_remove,X):
    """ removes run name_to_remove from X (list of vars) and Names - e.g. if it is an outlier """
    ind = Names.index(name_to_remove)
    Names = Names[:ind]+Names[ind+1:]
    Xnew = []
    for x in X:
      x = np.concatenate((x[:ind],x[ind+1:]),axis=0)
      Xnew.append(x)
    return(Names,Xnew)
