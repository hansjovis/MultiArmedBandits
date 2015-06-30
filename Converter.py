from copy import copy, deepcopy

""" mapping converts strings to ints and vice versa by first calling
    the variable name and then the value like mapping[var](val)
"""
mapping = {'header': lambda v: {'5':0, '15':1, '35':2,
                                0:'5', 1:'15', 2:'35'}[v],
           'adtype': lambda v: {'square':0, 'banner':1, 'skyscraper':2,
                                0:'square', 1:'banner', 2:'skyscraper'}[v],
           'color':  lambda v: {'red':0, 'green':1, 'blue':2, 'white':3, 'black':4,
                                0:'red', 1:'green', 2:'blue', 3:'white', 4:'black'}[v],
           'productid': lambda v: int(v+10) if type(v) is str else str(int(v)+10),
           'price':     lambda v: float(v) if type(v) is str else str(v),
           'ID':        lambda v: int(v) if type(v) is str else str(v),
           'Agent':     lambda v: {'OSX':0, 'Linux':1, 'Windows':2, 'mobile':3,
                                   0:'OSX', 1:'Linux', 2:'Windows', 3:'mobile'}[v],
           'Language': lambda v: {'EN':0, 'NL':1, 'GE':2,
                                  0:'EN', 1:'NL', 2:'GE'}[v],
           'Referer':  lambda v: {'Bing':0, 'Google':1, 'NA':2,
                                  0:'Bing', 1:'Google', 2:'NA'}[v],
           'Age':      lambda v: int(v) if type(v) is str else str(v)#,
          }

""" Keylist is the list of all keys to convert a dictionary to a tuple
    Its context_keys + choice_keys
    in the sequence that getcontext provides them
    and proposepage expects them
"""
KEYLIST = ['ID', 'Agent', 'Language', 'Age',  'Referer','header', 'adtype', 'color', 'productid', 'price']



def convert(inp, containertype=dict, valuetype=int, contextorchoices='both'):
    """ Converts the input to containertype with values of valuetype.
        containertype is dict or tuple
        valuetype is int or str
        contextorchoices is context or choices or both
    """
    inp = copy(inp)
    ctype = type(inp)
    vtype = type(inp[0 if ctype is tuple else inp.keys()[0]])
    start = 0 if contextorchoices in ['both', 'context'] else 5
    if ctype is not containertype:
        if containertype is tuple:
            # Only grab the five or ten values you need
            inp = dict2tup(inp)
        else:
            inp = tup2dict(inp, start)
    if vtype is not valuetype:
        if valuetype is str:
            inp = str2int(inp, start)
        else:
            inp = int2str(inp, start)
    return inp

def int2str(v, index=None):
    """Converts a tuple or dictionary or value to string"""
    if index is None:
        index = 0
    if type(v) is int:
        return mapping[index](v)
    elif type(v) is tuple:
        return tuple(int2str(vi, KEYLIST[index+i]) for i,vi in enumerate(v))
    elif type(v) is dict:
        return dict((k, int2str(vi, k)) for k,vi in v.iteritems())
    else:
        return v
    
def context_intify(context):
	new = {}
	for key in context:
		value = context[key]
		if type(value) in [str, unicode]:
			new.update({key: mapping[key](value)})
		else:
			new.update({key: value})
	return new

def choice_stringify(choice):
	new = {}
	for key in choice:
		value = choice[key]
		if type(value) is not str:
			new.update({key: mapping[key](value)})
		else:
			new.update({key: value})
	return new

def choice_intify(choice):
	new = {}
	for key in choice:
		value = choice[key]
		if type(value) is str:
			new.update({key: mapping[key](value)})
		else:
			new.update({key: value})
	return new

def str2int(v):
    """ Converts (tuple or dictionary of) strings to int according to mapping """
    if type(v) is str:
        return mapping[index](v)
    elif type(v) is tuple:
        return tuple(str2int(vi, i) for i,vi in enumerate(v))
    elif type(v) is dict:
        return dict((k, str2int(vi, k)) for k,vi in v.iteritems())
    else:
        return v
    
def dict2tup(d):
    """ Expects a dictionary and converts all keys in it to a tuple """
    return tuple(d[k] for k in KEYLIST if k in d)
    
def tup2dict(t, start=0):
    """ Expects a tuple or list with both context and choices """
    return dict(zip(KEYLIST[start:], t))
