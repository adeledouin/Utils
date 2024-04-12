# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:06:50 2019

@author: Victor
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib import cm
from matplotlib import collections as mc

# general parameters
empty_array = np.array([])*1.

#low boudaries for grain to touch = 0.00587663 m
#high boudaries for grain to touch = 0.00734579085 m
#spd_durus = 1200 m/s, bloc non contraint

network_param_example = (0.00587663, 0.00734579085, 1200, 2_000_000)

#########################################################################################################
# Module_Plot and properties definitions
#########################################################################################################

class Network:
    def __init__(self, x, y, r, strain, network_param, strains_contact = []):
        '''
        Initialisation of objects from the Network class.

        self: self

        x: list of x positions of the beads detected with Hough Transform
        y: "-----" y "---------------------------------------------------"
        r: list of radii of the beads "-----------------------------------"

        strain: list of strain on the beads, computed with eval_strain

        network_param: general parameters of the network

        strains_contact: list of strain around the contact, computed with
        eval_strain_contacts. If strains_contact is not an empty list, strain
        is not used for speed computations.

        '''
        spd_durus, sampling_freq, ratio = network_param

# General properties
        self.sampling_freq = sampling_freq
        self.spd_durus = spd_durus
        self.ratio = ratio # pixel to meter value
# Grain properties
        self.x_g = x # x centers of the grains
        self.y_g = y # y centers of the grain_signal
        self.r_g = r # radii of the grains
        self.strain = strain # strain of the GRAINS
        self.strains_contacts = strains_contact # strains around the CONTACTS
        self.n_part = len(self.x_g) # number of grains
        self.distances_grain = empty_array # distance between each grains
        self.angles_grain = empty_array # angles between each grains
# Contact properties
        self.n_contact = 0 # number of contacts
        self.x_c = [] # x position of contacts
        self.y_c = [] # y position of contacts
        self.speed_contact = empty_array # speed array of contacts (adjacency matrix)
        self.grain_in_contact = [] # List of ID of grains in cntact -> ex : [[0,10], [0, 176], [1, 35]..]
        self.sensor_id = []
        self.timefunc = lambda x : x # transform strain to speed. Identity because we directly give speeds
# Dijsktra tools
        self._nodes = set()
        self._edges = defaultdict(list)
        self._distances = {}
        self._speed = {}
        self.origin = 0
        self.visited = None
        self.path = None
# Graphical tools
        self.XG = empty_array
        self.YG = empty_array
        self.XC = empty_array
        self.YC = empty_array
        self.cmap = cm.viridis
        self.fig = None
        self.ax = None
# Initialisation methods
        self.calc_distances_grain() # computes the distances between the grains
        self.calc_angles_grain() # computes the angles between the grains
        self.calc_pos_contact() # computes the positions of the contacts
        self.calc_distances_contact() # computes the distances between the contacts
        if len(self.strains_contacts) > 0:
            # use this function only if strain_contacts is provided
            self.calc_speed_contact_bis()
        else:
            # otherwise use the old one
            self.calc_speed_contact()
        self.calc_flighttime() # computes the time for the soundwave to go from one contact to a neighboring contact
        self.calc_meshes()
        self.calc_node_and_edges()
        self.dijsktra()

    def reset(self):
        self.calc_flighttime()
        self.calc_meshes()
        self.calc_node_and_edges()


#########################################################################################################
# Init methods
#########################################################################################################

    def calc_distances_grain(self):
        '''
        Computation of the distances between every beads.
        '''
        dx = (self.x_g[None, :] - self.x_g[:, None])**2
        dy = (self.y_g[None, :] - self.y_g[:, None])**2
        SR = self.r_g[None, :] + self.r_g[:, None]

        self.distances_grain = (dx + dy)**0.5
#        f1 = self.distances_grain < self.low
#        f2 = self.distances_grain > self.high
        fd = (dx+dy)**0.5 > 1.05*SR # more than 5% diff in R1+R2 and D(1, 2)
        self.distances_grain[fd] = -1

    def calc_angles_grain(self):
        '''
        Computation of the angles between each bead.
        '''
        dx = (self.x_g[None, :] - self.x_g[:, None])
        dy = (self.y_g[None, :] - self.y_g[:, None])
        self.angles_grain = np.arctan2(dy, dx)

    def calc_pos_contact(self):
        '''
        Computes the list of grains in contact. It is stored
        in self.grain_in_contact, and the position of the contacts are stored
        in self.x_c and self.y_c
        The number of contacts is stored in self.n_contact
        '''
        for i in range(self.n_part):
            for j in range(i+1, self.n_part):
                dist = self.distances_grain[i, j]
                if dist != -1:
                    r1, r2 = self.r_g[i], self.r_g[j]
                    x1, x2 = self.x_g[i], self.x_g[j]
                    y1, y2 = self.y_g[i], self.y_g[j]
                    _sr = 1/(r1+r2)
                    self.x_c += [(r2*x1 + r1*x2) * _sr]
                    self.y_c += [(r2*y1 + r1*y2) * _sr]
                    self.grain_in_contact += [[i,j]]
        self.x_c, self.y_c = np.array(self.x_c), np.array(self.y_c)
        self.grain_in_contact = np.array(self.grain_in_contact)
        self.grain_in_contact.sort(1)
        self.n_contact = len(self.x_c)

    def neighboring_contact(self, i):
        '''
        Finds the neighboring contacts of contact i.
        '''
        g1, g2 = self.grain_in_contact[i]
        L1 = list(np.where(self.grain_in_contact == g1)[0])
        L2 = list(np.where(self.grain_in_contact == g2)[0])
        return np.array(list(set(L1+L2)))

    def common_grain(self, contact_i, contact_j):
        '''
        Finds the common grain of contact_i and contact_j, i.e. the grain
        that is a part of contact_i and contact_j.
        '''
        g1i, g2i = self.grain_in_contact[contact_i]
        g1j, g2j = self.grain_in_contact[contact_j]
        if g1i in [g2i, g2j]:
            return g1i
        else:
            return g2j

    def calc_distances_contact(self):
        ''' Computes all the distances between every contact, and stores it
        into a matrix called self.distances_contact'''
        dx = (self.x_c[None, :] - self.x_c[:, None])**2
        dy = (self.y_c[None, :] - self.y_c[:, None])**2
        self.distances_contact = (dx + dy)**0.5

        mask = np.zeros_like(self.distances_contact)
        for i in range(self.n_contact):
            mask[i][self.neighboring_contact(i)] = 1
        self.distances_contact *= mask

    def calc_speed_contact(self):
        ''' Computes the speed at which the soundwave travel between two contacts,
        using the strain of the grain in which it travel. This grain is the common grain
        of the two contacts. Stores it in a weighted adjacency matrix called
        self.speed_contact. This means the speed between contact i and contact j is
        stord in self.speed_contact[i,j] (or self.speed_contact[j,i]) '''
        self.speed_contact = np.ones_like(self.distances_contact)
        for i in range(self.n_contact):
            contacts = self.neighboring_contact(i)
            for j in contacts:
                common_grain = self.common_grain(i, j)
                self.speed_contact[i, j] = self.timefunc(self.strain[common_grain])

    def calc_speed_contact_bis(self):
        '''
        Computes the speed at which the soundwave travel between two contacts,
        using the mean of the strain around each of the contact.  Stores it in
        a weighted adjacency matrix called self.speed_contact.
        This means the speed between contact i and contact j is stored in
        self.speed_contact[i,j] (or self.speed_contact[j,i])

        '''
        self.speed_contact = np.ones_like(self.distances_contact)
        for i in range(self.n_contact):
            contacts = self.neighboring_contact(i)
            for j in contacts:
                s1, s2 = self.strains_contacts[i], self.strains_contacts[j]
                S = np.mean([s1,s2])
                self.speed_contact[i,j] = self.timefunc(S)

    def calc_flighttime(self):
        '''
        Computes the flighttime between the contacts, using the distances between
        them and the speed. If we assume a constant speed between the contact,
        flighttime = distance / speed
        Stored in a weighted adjacency matrix.
        '''
        self.flighttime = self.distances_contact / self.speed_contact
        self.flighttime *= self.sampling_freq
        self.flighttime[self.flighttime==0] = -1


    def calc_node_and_edges(self):
        '''
        Creating the nodes and edges lists, weighting the edges with self.flighttime
        '''
        for i in range(len(self.flighttime)):
            self._add_node(i)
            r = self.flighttime[i]
            s = self.speed_contact[i]
            for j in range(len(r)):
                if r[j] != -1:
                    self._add_edge(i, j, r[j], s[j])
       #print('Dijsktra with default origin...')
        self.dijsktra()

    def _add_node(self, value):
        """ Dijsktra support function """
        self._nodes.add(value)

    def _add_edge(self, from_node, to_node, distance, speed):
        """ Dijsktra support function """
        self._edges[from_node].append(to_node)
        self._edges[to_node].append(from_node)
        self._distances[(from_node, to_node)] = distance
        self._speed[(from_node, to_node)] = speed

    def calc_meshes(self):
        XC, YC = np.meshgrid(self.x_c, self.y_c)
        XG, YG = np.meshgrid(self.x_g, self.y_g)
        self.XC, self.YC = XC.flatten(), YC.flatten()
        self.XG, self.YG = XG.flatten(), YG.flatten()

        XC = (self.x_c[:,None] + self.x_c[None,:])/2
        YC = (self.y_c[:,None] + self.y_c[None,:])/2
        self.XC, self.YC = XC.flatten(), YC.flatten()

    def add_frame_contacts(self, x_capts, y_capts, x_cont, y_cont, grains_touching):
        """ A appeler 3 fois en tout, pour chaque bati """

####### init
        n_new  = len(x_capts) + len(x_cont)
        new_n_contact = self.n_contact + n_new
        self.sensor_id += [i + self.n_contact + len(x_cont) for i in range(len(x_capts))]
        x_new_c = np.concatenate((x_cont, x_capts))
        y_new_c = np.concatenate((y_cont, y_capts))

####### ajouter les distances
        new_distances_contact = np.zeros([new_n_contact, new_n_contact])
        new_distances_contact[:self.n_contact, :self.n_contact] = 1. * self.distances_contact

        for i in range(n_new):
            for j in range(n_new):
                dist2 = (x_new_c[i] - x_new_c[j])**2 + (y_new_c[i] - y_new_c[j])**2
                new_distances_contact[i + self.n_contact, j + self.n_contact] = dist2 ** 0.5

        for grain, c in zip( grains_touching, range(len(x_cont)) ):
            existing_contacts = np.where(self.grain_in_contact == grain)[0]
            for e_c in existing_contacts:
                dist2 = (x_new_c[c] - self.x_c[e_c])**2 + (y_new_c[c] - self.y_c[e_c])**2
                new_distances_contact[e_c, c + self.n_contact] = dist2 ** 0.5
                new_distances_contact[c + self.n_contact, e_c] = dist2 ** 0.5
        self.distances_contact = new_distances_contact

####### ajouter les vitesses
        new_speed_contact = np.ones([new_n_contact, new_n_contact])
        new_speed_contact[:self.n_contact, :self.n_contact] = 1. * self.speed_contact

        for i in range(n_new):
            for j in range(n_new):
                new_speed_contact[i + self.n_contact, j + self.n_contact] = self.spd_durus

        for grain, c in zip( grains_touching, range(len(x_cont)) ):
            existing_contacts = np.where(self.grain_in_contact == grain)[0]
            for e_c in existing_contacts:
                new_speed_contact[e_c, c + self.n_contact] = self.spd_durus
                new_speed_contact[c + self.n_contact, e_c] = self.spd_durus
        self.speed_contact = new_speed_contact

####### re-calc les flight time, finaliserw
        self.n_contact = new_n_contact
        self.x_c = np.concatenate((self.x_c, x_new_c))
        self.y_c = np.concatenate((self.y_c, y_new_c))
        self.calc_flighttime()
        self.calc_meshes()
        self.calc_node_and_edges()


    def add_sensor_contacts(self, touching, x_capts, y_capts):

        x_capts = x_capts.flatten() ; y_capts = y_capts.flatten()
        touching = touching.astype('int')
        new_n_contact = self.n_contact + len(x_capts)

        x_new_c = np.concatenate((self.x_c, x_capts))
        y_new_c = np.concatenate((self.y_c, y_capts))

        new_distances_contact = np.zeros([new_n_contact, new_n_contact])
        new_distances_contact[:self.n_contact, :self.n_contact] = 1. * self.distances_contact
        for ic, (xc, yc) in enumerate(zip(x_capts, y_capts)):
            for t in touching[ic]:
                dist2 = (self.x_c[t] - xc)**2 + (self.y_c[t] - yc)**2
                new_distances_contact[ic + self.n_contact, t] = dist2 ** 0.5
                new_distances_contact[t, ic + self.n_contact] = dist2 ** 0.5

        new_speed_contact = np.ones([new_n_contact, new_n_contact])
        new_speed_contact[:self.n_contact, :self.n_contact] = 1. * self.speed_contact
        for ic, (xc, yc) in enumerate(zip(x_capts, y_capts)):
            for t in touching[ic]:
                new_speed_contact[ic + self.n_contact, t] = self.spd_durus
                new_speed_contact[t, ic + self.n_contact] = self.spd_durus

        self.sensor_id += [i + self.n_contact for i in range(len(x_capts))]
        self.distances_contact = new_distances_contact
        self.speed_contact = new_speed_contact
        self.x_c = x_new_c
        self.y_c = y_new_c
        self.n_contact = new_n_contact
        self.calc_flighttime()
        self.calc_meshes()
        self.calc_node_and_edges()

#########################################################################################################
# Shortest path algorithm
#########################################################################################################

    def reverse_propagation(self, sensor_num):
        self.dijsktra(self.sensor_id[sensor_num])

    def reverse_propagation_shifts(self, contact):
        self.dijsktra(contact) ; out = []
        for sensor in self.sensor_id:
            out += [self.visited[sensor]]
        return out

    def reverse_propagation_smart(self):
        ttime = np.zeros([len(self.sensor_id), self.n_contact])
        for i, sensor in enumerate(self.sensor_id):
            self.dijsktra(sensor)
            for point in range(self.n_contact):
                try:
                    ttime[i, point] = self.visited[point]
                except:
                    ttime[i, point] = np.inf
        return ttime


    def dijsktra(self, initial=-1):
        if initial == -1:
            initial = self.origin
        else:
            self.origin = initial
        visited = {initial: 0}
        path = {}
        nodes = set(self._nodes)
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break
            nodes.remove(min_node)
            current_weight = visited[min_node]
            for edge in self._edges[min_node]:
                weight = current_weight + self._distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
        self.visited = visited
        self.path = path


    def find_path(self, source, target):
        self.dijsktra(source)
        path = [target]
        while path[-1] != source:
            path += [self.path[path[-1]]]
        return path

########################################################################################################
#Plot methods
########################################################################################################

    def plot(self):
        if self.fig is None:
            self.fig, self.ax = plt.subplots()
            self.ax.axis('equal')

    def new_plot(self):
        self.fig, self.ax = plt.subplots()
        self.ax.axis('equal')

    def close_plot(self):
        if self.fig is None:
            print('No axis to close')
        else:
            plt.close(self.fig)
            self.fig, self.ax = None, None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    def rep_net(self):
        self.plot()
        edgelist = self.distances_contact
        L = []
        for i, line in enumerate(edgelist):
            for j in np.where(line>0)[0]:
                L +=[
                  [(self.y_c[i], -self.x_c[i]), (self.y_c[j], -self.x_c[j])]]
        lc = mc.LineCollection(L, colors='k')
        self.ax.add_collection(lc)
        self.ax.autoscale()

    def rep_contact(self):
        self.plot()
        plt.scatter(self.y_c, -self.x_c, color = 'k', marker='.')
        for i, (x, y) in enumerate(zip(self.x_c, self.y_c)):
            self.ax.annotate(i, (y, -x))

    def rep_path(self, source, target):
        path = self.find_path(source, target)
        line_x, line_y = [], []
        for point in path:
            line_x += [self.x_c[point]]
            line_y += [self.y_c[point]]
        line_x = np.array(line_x)
        line_y = np.array(line_y)
        plt.plot(line_y, -line_x, 'r', linewidth=5)

    def rep_wave(self, t_ref=0):
        self.plot() #self.rep_net()
        K = list(self.visited.keys())
        val = list(self.visited.values())
        M = max(self.visited.values())
        if t_ref == 0:
            t_ref = M
        x, y = self.x_c[K], self.y_c[K]
        #c = np.modf(np.linspace(0, .9999 * M / t_ref, self.n_contact))[0]
        c = np.array(val)/M
        tr, t1, t2 = str(M)[:5], str(t_ref/5)[:5], str(t_ref/20)[:5]
        self.ax.set_title(
                'total: ' + tr + 's [hue=' + t1 + 's, sat=' + t2 + 's]')
        self.ax.scatter(y, -x, color=self.cmap(c), zorder=3)
        x0, y0 = self.x_c[self.origin], self.y_c[self.origin]
        plt.plot(y0, -x0, 'kp', zorder=3, markersize=15)

    def rep_flighttime(self):
        self.plot()
      #  self.rep_net()
        flightimes = self.flighttime
        flightimes[flightimes==-1] = np.nan
        plt.scatter(self.XC, self.YC, c = self.flighttime.flatten())

    def rep_grain(self, stress=True):
        self.plot()
        grains = []
        for i, (x, y, r, s) in enumerate(zip(self.x_g, self.y_g, self.r_g, self.strain)):
            if stress:
                c = (s - self.strain.min())/(self.strain.max() - self.strain.min())
                grains += [plt.Circle((y, -x), r, fill=True, color=self.cmap(c))]
            else:
                grains += [plt.Circle((y, -x), r, fill=False, color = 'k')]
                self.ax.annotate(i, (y, -x))

        for grain in grains:
            self.ax.add_artist(grain)
        self.ax.set_xlim(self.x_g.min()-50, self.x_g.max()+50)
        self.ax.set_ylim(self.y_g.min()-50, self.y_g.max()+50)




#########################################################################################################
# PURGATORY
#########################################################################################################


    # def calc_speed(self):
    #     '''
    #     Useless ?
    #     '''
    #     self.force = 1.*self.distances
    #     self.force[self.distances < self.low] = -1
    #     self.force[self.distances > self.high] = -1
    #     for i, j in zip(range(self.n_part), range(self.n_part)):
    #         if self.force[i,j] != 1:
    #             self.force[i,j] = min(self.strain[i], self.strain[j])
    #     self.speed = self.timefunc(self.force)
