from Utils.Module_Plot.classPlot import *
from Utils.Module.UDgate.fct_UDgate import *

plot = PaperPlot(remote=False)

# %% ################### Function UDGate ##################################

#### verifier les indices des chutes
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
udg = UDgate(w=10, h=4)
plot.plt.plot(np.arange(udg.size)*1e-4, udg, '.--', label='UDgate victor')
udg = UDgate_asymetric(w=10, h=4)
plot.plt.plot(np.arange(udg.size)*1e-4, udg, '.--', label='UDgate asymetric')
udg = UDgate_asymetric(w=10, h=4, forward=False)
plot.plt.plot(np.arange(udg.size)*1e-4, udg, '.--', label='UDgate asymetric')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

# %% ################### Function convolution ##################################

# f = sub_batch.f
f = np.array([0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, 0, 0, 0, 0])
t = np.arange(f.size) ##  sub_batch.t_V ##

## ### forward
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.convolve(f, UDgate(w=1, h=0), mode='valid')
der_b_2 = np.convolve(f, UDgate(w=1, h=2), mode='valid')
der_b_3 = np.convolve(f, UDgate(w=1, h=4), mode='valid')
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-7, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### backward
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = - np.convolve(-f[::-1], UDgate(w=1, h=0), mode='valid')
der_b_2 = - np.convolve(-f[::-1], UDgate(w=1, h=2), mode='valid')
der_b_3 = - np.convolve(-f[::-1], UDgate(w=1, h=4), mode='valid')
plot.plt.plot(t, -f[::-1], '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=3, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### forward asymetric
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.convolve(f, UDgate_asymetric(w=1, h=0), mode='valid')
der_b_2 = np.convolve(f, UDgate_asymetric(w=1, h=2), mode='valid')
der_b_3 = np.convolve(f, UDgate_asymetric(w=1, h=4), mode='valid')
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-7, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### backward asymetric
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=0), mode='valid')
der_b_2 = - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=2), mode='valid')
der_b_3 = - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=4), mode='valid')
plot.plt.plot(t, -f[::-1], '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=3, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)


## ### forward asymetric avec mean
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.convolve(f, UDgate_asymetric(w=3, h=0), mode='valid')
der_b_2 = np.convolve(f, UDgate_asymetric(w=3, h=2), mode='valid')
der_b_3 = np.convolve(f, UDgate_asymetric(w=3, h=4), mode='valid')
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-7, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### backward asymetric avec mean
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=0, forward=False), mode='valid')
der_b_2 = - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=2, forward=False), mode='valid')
der_b_3 = - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=4, forward=False), mode='valid')
plot.plt.plot(t, -f[::-1], '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=3, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### forward asymetric good shape
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.hstack((np.convolve(f, UDgate_asymetric(w=1, h=0), mode='valid'), np.zeros(1+0)))
der_b_2 = np.hstack((np.convolve(f, UDgate_asymetric(w=1, h=2), mode='valid'), np.zeros(1+2)))
der_b_3 = np.hstack((np.convolve(f, UDgate_asymetric(w=1, h=4), mode='valid'), np.zeros(1+4)))
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-7, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### backward asymetric good shape
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.hstack((np.zeros(0), - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=0, forward=False), mode='valid'), np.zeros(0+1)))[::-1]
der_b_2 = np.hstack((np.zeros(0), - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=2, forward=False), mode='valid'), np.zeros(2+1)))[::-1]
der_b_3 = np.hstack((np.zeros(0), - np.convolve(-f[::-1], UDgate_asymetric(w=1, h=4, forward=False), mode='valid'), np.zeros(4+1)))[::-1]
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-4, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### forward asymetric with mean
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.convolve(f, UDgate_asymetric(w=3, h=0), mode='valid')
der_b_2 = np.convolve(f, UDgate_asymetric(w=3, h=2), mode='valid')
der_b_3 = np.convolve(f, UDgate_asymetric(w=3, h=4), mode='valid')
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-7, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

## ### backward asymetric with mean
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
der_b_1 = np.hstack((np.zeros(3-1), - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=0, forward=False), mode='valid'), np.zeros(0+1)))[::-1]
der_b_2 = np.hstack((np.zeros(3-1), - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=2, forward=False), mode='valid'), np.zeros(2+1)))[::-1]
der_b_3 = np.hstack((np.zeros(3-1), - np.convolve(-f[::-1], UDgate_asymetric(w=3, h=4, forward=False), mode='valid'), np.zeros(4+1)))[::-1]
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(der_b_1, '.-', label='h=0')
plot.plt.plot(der_b_2, '.-', label='h=2')
plot.plt.plot(der_b_3, '.-', label='h=4')
ax.axvline(x=f.size-4, c='k')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)
#
# # %% ################### derivée sur signal "parfait" ##################################

# f = sub_batch.f
f = np.array([0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, 0, 0, 0, 0])
t = np.arange(f.size) ##  sub_batch.t_V ##

## ### h trop petit
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_,  der = convo_shift(f, w=1, h=0)
_, der_b = convo_shift(f, w=1, h=0, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))

## ### h parfait
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=1, h=2)
_, der_b = convo_shift(f, w=1, h=2, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))


## ### h trop grand
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=1, h=4)
_, der_b = convo_shift(f, w=1, h=4, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))

# %% ################### derivée sur signal avec oscillations ##################################

# f = sub_batch.f
f = np.array([0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, -2, 2, -1, 1, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, -2, 2, -1, 1, 0, 0, 0, 0,])
t = np.arange(f.size) ##  sub_batch.t_V ##

## ### h trop petit
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=1, h=0)
_, der_b = convo_shift(f, w=1, h=0, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))

## ### h parfait
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=1, h=2)
_, der_b = convo_shift(f, w=1, h=2, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))


## ### h trop grand
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=1, h=4)
_, der_b = convo_shift(f, w=1, h=4, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))

## ### h trop grand + w forward
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f, w=4, h=4)
_, der_b = convo_shift(f, w=4, h=4, forward=False)
# der_b = convo_shift(f, w=4, h=4), forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(der)))
print("cbackward trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f), np.max(-der_b)))


# # # %% ################### derivée sur signal "bruité" ##################################

# f = sub_batch.f
f = np.array([0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, -2, 2, -1, 1, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 5, 2, -2, 2, -1, 1, 0, 0, 0, 0,])
t = np.arange(f.size) ##  sub_batch.t_V ##

noise = np.random.normal(0, 0.3, f.size)

## ### h trop petit
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f+noise, w=1, h=0)
_, der_b = convo_shift(f+noise, w=1, h=0, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(der)))
print("cbackward h trop petit : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(-der_b)))

## ### h parfait
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f+noise, w=1, h=2)
_, der_b = convo_shift(f+noise, w=1, h=2, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(der)))
print("cbackward parfait : chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(-der_b)))


## ### h trop grand
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f+noise, w=1, h=4)
_, der_b = convo_shift(f+noise, w=1, h=4, forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(der)))
print("cbackward trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(-der_b)))

## ### h trop grand + w forward
fig, ax = plot.belleFigure('$t \ (s)$', '$convolution$', nfigure=None)
_, der = convo_shift(f+noise, w=4, h=4)
_, der_b = convo_shift(f+noise, w=4, h=4, forward=False)
# der_b = convo_shift(f+noise, w=4, h=4), forward=False)
plot.plt.plot(t, f, '.-', color='silver')
plot.plt.plot(t, der, 'C0.-', label='conv shift forward')
plot.plt.plot(t, der_b, 'C1.-', label='conv shift backward')
plot.plt.grid(True, which='both')
plot.plt.legend(loc="best")
save = None
plot.fioritures(ax, fig, title=None, label=True, grid=None, save=save)

print("forward h trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(der)))
print("cbackward trop grand: chute max Df = {} | chute max trouvée en der f = {}".format(np.max(f+noise), np.max(-der_b)))
