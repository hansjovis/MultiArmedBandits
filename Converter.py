from copy import copy, deepcopy

""" mapping converts strings to ints and vice versa by first calling
    the variable name and then the value like mapping[var](val)
"""
mapping = {'header': lambda v: {'5':0, '15':1, '35':2,
                                0:'5', 1:'15', 2:'35'}[v]
           'adtype': lambda v: {'square':0, 'banner':1, 'skyscraper':2,
                                0:'square', 1:'banner', 2:'skyscraper'}[v]
           'color':  lambda v: {'red':0, 'green':1, 'blue':2, 'white':3, 'black':4,
                                0:'red', 1:'green', 2:'blue', 3:'white', 4:'black'}[v]
           'productid': lambda v: int(v) if type(v) is str else str(v)
           'price':     lambda v: float(v) if type(v) is str else str(v)
           'ID':        lambda v: int(v) if type(v) is str else str(v)
           'Agent':     lambda v: {'OSX':0, 'Linux':1, 'Windows':2, 'mobile':3,
                                   0:'OSX', 1:'Linux', 2:'Windows', 3:'mobile'}[v]
           'Language': lambda v: {'EN':0, 'NL':1, 'GE':2,
                                  0:'EN', 1:'NL', 2:'GE'}[v]
           'Referer':  lambda v: {'Bing':0, 'Google':1, 'NA':2,
                                  0:'Bing', 1:'Google', 2:'NA'}[v]
           'Age':      lambda v: int(v) if type(v) is str else str(v)
          }

""" Keylist is the list of all keys to convert a dictionary to a tuple
    Its context_keys + choice_keys
    in the sequence that getcontext provides them
    and proposepage expects them
"""
KEYLIST = ['ID', 'Agent', 'Language', 'Referer', 'Age', 'header', 'adtype', 'color', 'productid', 'price']



def convert(inp, containertype=dict, valuetype=int)
    """ Converts the input to containertype with values of valuetype.
        containertype is dict or tuple
        valuetype is int or str
    """
    inp = copy(inp)
    ctype = type(inp)
    vtype = type(inp[0 if ctype is tuple else inp.keys[0]])
    if ctype is not containertype:
        if ctype is dict:
            inp = tup2dict(inp)
        else:
            inp = dict2tup(inp)
    if vtype is not valuetype:
        if vtype is str:
            inp = int2str(inp)
        else:
            inp = str2int(inp)
    return inp

def int2str(v, index=None):
    """Converts a tuple or dictionary or value to string"""
    if type(v) is int:
        return mapping[index](v)
    elif type(v) is tuple:
        return tuple(int2str(vi, i) for i,vi in enumerate(v))
    elif type(v) is dict:
        return dict(int2str(vi, k) for k,vi in v.iteritems())
    else
        return v
    
def str2int(v, index=None):
    """ Converts (tuple or dictionary of) strings to int according to mapping """
    if type(v) is str:
        return mapping[index](v)
    elif type(v) is tuple:
        return tuple(str2int(vi, i) for i,vi in enumerate(v))
    elif type(v) is dict:
        return dict(str2int(vi, k) for k,vi in v.iteritems())
    else
        return v
    
def dict2tup(d):
    """ Expects a dictionary and converts all keys in it to a tuple """
    return tuple(d[k] for key in KEYLIST if key in d)
    
def tup2dict(t):
    """ Expects a tuple or list with both context and choices """
    return dict(zip(KEYLIST, t))
