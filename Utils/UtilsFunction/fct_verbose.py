import inspect
from time import ctime


def printv(message, is_debug=False, verbose = True, show_debug = True):
    """ conditional print function, if verbose=True. Will also display
    caller function name and UTC time before message. """
    if verbose:
        context_len = 30 ; fchar = ' '
        if is_debug:
            message = 'DEBUG : '+ str(message)
            fchar = '-'
        if (show_debug and is_debug) or not is_debug:
            try:
                caller_name = (inspect.stack()[1].function).upper()
            except:
                caller_name = (inspect.stack()[1][3]).upper()
            caller_name = caller_name.ljust(context_len, fchar)
            date = ctime()
            context = '[{}, {}]:'.format(caller_name, date)
            print(context, message, flush=True)
