import numpy as np

# ------------------------------------------
def UDgate(w, h):
    """
    ---,_|¨l---
    """
    x0 = w + h // 2
    out = np.zeros(2 * w + h)
    out[:x0 - h // 2] = -1.
    out[x0 + h // 2:] = 1.
    # out[x0-h/2:x0+h/2] = np.linspace(-1,1,h)
    return out / (1. * w)

# ------------------------------------------
def UDgate_asymetric(w, h, forward=True):
    """
    ---,_|¨l---
    """
    x0 = w + h // 2
    out = np.zeros(w + h + 1)
    if forward:
        out[:x0 - h//2:] = -1. / (1. * w)
        out[-1] = 1.
    else:
        out[0] = -1.
        out[h+1:] = 1. / (1. * w)
    # out[x0-h/2:x0+h/2] = np.linspace(-1,1,h)
    return out

# ------------------------------------------
def convo_shift(signal, w, h, forward=True):
    if forward:
        udg = UDgate_asymetric(w=w, h=h)
        out = np.hstack((np.convolve(signal, udg, mode='valid'), np.zeros(h+w)))
    else:
        udg = UDgate_asymetric(w=w, h=h, forward=False)
        out = np.hstack((np.zeros(w-1), -np.convolve(-signal[::-1], udg, mode='valid'), np.zeros(h+1)))[::-1]
    return udg, out

# ------------------------------------------
def UDgate_asym(w, h, forward=True):
    out = np.zeros(w + h)
    if forward:
        out[0] = -1.
        out[1+h:] = 1. / (1. * w)
    else:
        out[:w+1] = -1.
        out[h:] = 1. / (1. * w)
    return out

# ------------------------------------------
def convo(signal, udg):
    l = len(udg) // 2
    out = np.convolve(signal, udg, mode='same')
    out[:l] = 0
    out[-l:] = 0
    return out

# ------------------------------------------
def loose_info_size(w, h):
    return UDgate(w, h).size