import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import read_data
import network
import networkx as nx 
import myclass as mc
import copy
import mypara 



if __name__ == "__main__":
    """
        main program
    """
    # step 0: set the intitl para class
    para = mypara.ParaClass() 
    # step 1: read data
    net = read_data.read_data()
    # step 2: Create paths 
    # step 2.1. convert my network to networkx data
    G = network.create_netx_graph(net) 
    # step 2.2 create paths 
    paths = []
    counter = 0
    for w in net.ODs:
        # add one more
        for m in w.modes:
            #TODO: Here you need to address different modes
            #TODO: given mode m, if mode can not travel a link, set the link weight to very large, before find the simple paths
            #TODO: after solveing, you may change the large number to be the origin weight number
            for path in nx.all_simple_edge_paths(G, source= w.origin, target= w.dest): # generate all paths 
                print(path)
                paths.append(mc.PathClass())
                paths[-1].id = counter
                paths[-1].edges = copy.deepcopy(path)
                paths[-1].od = w.id
                w.mode_path[m].append(paths[-1].id)
                counter =  counter + 1 
                # links = path # record links
                # link_sque =[G.edges[edge]['link_id'] for edge in path] # record links ID
                # name_sque = [G.edges[edge]['name'] for edge in path]
                # attribute_set = [G.edges[edge]['attribute'] for edge in path]            
                # paths.append([od_pair, links, link_sque, name_sque, attribute_set])

    print("pause and check") 
    
    #TODO: 1. check path generated for each mode/OD pair/
    # 2. write a function to print the path to a file 
    # 3. write a function to read the path from a file
    # 4. write a function to compute the logsum utiltiy for mode/nested modes 
    # Therefore, in the future tests, you only need to generate path set for once (then adjust the function to read)
    # 4. deal with cost of other links etc. 
    # 5. not sure about the fleet size updating method

    #TODO: MSA main
    # there are algorithms for solving nested logit model. 
    # Stochastic User Equilibrium Formulation for Generalized Nested Logit Model
    # (you can find more)
    # however, these studies formulated as minimistaiton problem for the assignment
    # which is not applicable for us, because of the consideration of the fleet size ?? 
    # Algorithm
    # level 1: assign flow between Auto/Combined, this needs an MSA updating method
    # level 2: assign flow between each mode, this is another MSA
    # level 3: assign flow to paths, this is a path MSA






    exit()
 
    
# warnings.filterwarnings('ignore')
__file__ = './'
# set parameter
theta_1 = 0.008# path 
theta_2 = 0.005 # mode
miu_in = 25
miu_out = 30
lamda_0_hailing = 2 #2 RMB/minute
lamda_0_PR = 20 # RMB
lamda_0_transit = 5
N_hailing = 600
lamda_0_auto = link.compute_lamda_0_auto(fuel_consumption=8.5)

res = msa.assignment(my_link= my_link, my_node= my_node, my_demand= my_demand,
                    origin_zone= origin_zone, destination_zone= destination_zone,
                    miu_in= miu_in, miu_out= miu_out,
                    lamda_0_auto = lamda_0_auto,
                    lamda_0_hailing= lamda_0_hailing,
                    lamda_0_transit= lamda_0_transit,
                    lamda_0_PR= lamda_0_PR,
                    theta_1= theta_1, theta_2= theta_2,
                    N_hailing= N_hailing, A=2, maximum_iter=300)

# RMSE
RMSE = res[0]

# idle ride-hailing vehicle number
ride_hailing = res[5]

# market share
mode = res[4]

# path flow
path = res[2]
path = path[['I','path_id', 'mode', 'path_flow', 'path_cost']]
path['path_cost'] = abs(path['path_cost'])

num_loc = 200
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

fig = plt.figure(figsize=(12,6))
ax1 = plt.subplot(1,2,1)
ax1.grid(ls = '--', lw = 0.5, zorder = 0)
ax1.plot(RMSE['I'].iloc[1:num_loc], RMSE['RMSE'].iloc[1:num_loc], '-', lw = 2, color='#0c5DA5', label='RMSE', markersize=5, zorder =1)
#ax1.set_xticks(np.arange(5, 105, 10))
#ax1.set_xlim(0, 101)
#ax1.set_yticks(np.arange(0, 0.55, 0.05))
#ax1.set_ylim(0, 0.5)
ax1.set_xlabel('Number of iterations')
ax1.set_ylabel('RMSE')
ax1.set_title('(a) Convergence criteria', fontsize=18, loc = 'center', y=1.02)

ax2 = plt.subplot(1,2,2)
ax2.grid(ls = '--', lw = 0.5)
ax2.plot(ride_hailing['I'].iloc[:100], ride_hailing['n_idle'].iloc[:100], '-', lw = 2, color='#0c5DA5', label='idle ride-hailing', markersize=5)
ax2.set_xlabel('Number of iterations')
ax2.set_ylabel('Idle ride-hailing vehiles')
# ax2.set_xticks(np.arange(5, 31, 5))
# ax2.set_xlim(0.5, 30.5)
# ax2.set_yticks(np.arange(155,210, 5))
# ax2.set_ylim(150,205)
ax2.set_title('(b) Convergence of ride-hailing', fontsize=18, y= 1.02)

ax3 = plt.twinx(ax2)
ax3.plot(ride_hailing['I'].iloc[:100], ride_hailing['wait_time'].iloc[:100], '--', lw = 2, color='#00B945', label='waiting time', markersize=4)
# ax3.set_yticks(np.arange(3.9, 4.7, 0.1))
# ax3.set_ylim(3.8,4.6)
ax3.set_ylabel('Waiting time for ride-hailing (min)')

ax2.legend(loc='best', fontsize=16, frameon=False, handlelength=1.5, bbox_to_anchor=(1, 0.8))
ax3.legend(loc='best', fontsize=16, frameon=False, handlelength=1.5, bbox_to_anchor=(0.93, 0.7))

plt.tight_layout()

plt.show()

# market share
num_loc = 100
#plt.ticklabel_format(style='plain')

fig,ax = plt.subplots(2,2, figsize=(15,15))
ax = ax.flatten()

ax1 = ax[0]
ax1.ticklabel_format(useOffset=False)
ax1.grid(ls='--', alpha = 0.5)
ax1.plot(mode[mode['mode'] == 'auto'].iloc[1:num_loc]['I'], 
         mode[mode['mode'] == 'auto'].iloc[1:num_loc]['mode_logit']*100, 
         '-', color='#0c5DA5', label='Auto', markersize=5, lw=2)
# ax1.set_xticks(np.arange(0, 205, 20))
# ax1.set_xlim(0.5, 50.5)
# ax1.set_yticks(np.arange(296.8, 298.4, 0.2))
#ax1.set_ylim(36.125,36.127)
ax1.set_xlabel('Number of iterations')
ax1.set_ylabel('Average market share (%)')
ax1.set_title('(a) Auto mode', fontsize=18, loc='center', y=1.02)

ax2 = ax[1]
ax2.ticklabel_format(useOffset=False)
ax2.grid(ls='--', alpha = 0.5)
ax2.plot(mode[mode['mode'] == 'transit'].iloc[1:num_loc]['I'], 
         mode[mode['mode'] == 'transit'].iloc[1:num_loc]['mode_logit']*100, 
         '-', color='#00b945', label='Transit', markersize=5, lw=2)
# ax1.set_xticks(np.arange(0, 205, 20))
# ax1.set_xlim(0.5, 50.5)
# ax1.set_yticks(np.arange(296.8, 298.4, 0.2))
#ax2.set_ylim(21.2512,21.2518)
ax2.set_xlabel('Number of iterations')
ax2.set_ylabel('Average market share (%)')
ax2.set_title('(b) Transit mode', fontsize=18, loc='center', y=1.02)

ax3 = ax[2]
ax3.ticklabel_format(useOffset=False)
ax3.grid(ls='--', alpha = 0.5)
ax3.plot(mode[mode['mode'] == 'P&R'].iloc[1:num_loc]['I'], 
         mode[mode['mode'] == 'P&R'].iloc[1:num_loc]['mode_logit']*100, 
         '-', color='#ff9500', label='P&R', markersize=5, lw=2)
# ax1.set_xticks(np.arange(0, 205, 20))
# ax1.set_xlim(0.5, 50.5)
# ax1.set_yticks(np.arange(296.8, 298.4, 0.2))
#ax3.set_ylim(19.7795,19.7810)
ax3.set_xlabel('Number of iterations')
ax3.set_ylabel('Average market share (%)')
ax3.set_title('(c) P&R mode', fontsize=18, loc='center', y=1.02)

ax4 = ax[3]
ax4.ticklabel_format(useOffset=False)
ax4.grid(ls='--', alpha = 0.5)
ax4.plot(mode[mode['mode'] == 'R&T'].iloc[1:num_loc]['I'], 
         mode[mode['mode'] == 'R&T'].iloc[1:num_loc]['mode_logit']*100, 
         '-', color='#ff2c00', label='R&T', markersize=5, lw=2)
# ax1.set_xticks(np.arange(0, 205, 20))
# ax1.set_xlim(0.5, 50.5)
# ax1.set_yticks(np.arange(296.8, 298.4, 0.2))
#ax4.set_ylim(22.8405,22.8440)
ax4.set_xlabel('Number of iterations')
ax4.set_ylabel('Average market share (%)')
ax4.set_title('(d) R&T mode', fontsize=18, loc='center', y=1.02)
plt.tight_layout()

plt.show()




