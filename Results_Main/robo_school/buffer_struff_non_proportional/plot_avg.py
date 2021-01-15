import torch
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

no_steps = 400000
n_step = int(no_steps/1000)
dir_name = "buff_size_50k/hrf_snr_ft"

changing_variable = [0.75, 1.75, 2.75, 3.75]
changing_variable_at = [0, 100, 150, 350]

load_dir_1 = "results_length__s_i_1000_1"
load_dir_2 = "results_length__s_i_1000_2"
load_dir_3 = "results_length__s_i_1000_3"
#load_dir_4 = "results_length__s_i_1000_4"
#load_dir_5 = "results_length__s_i_1000_5"

changing_variable_name = "power_avg"


legend = ["p = " + str(i) for i in changing_variable]

r1 = torch.load(dir_name + "/" + load_dir_1)
r2 = torch.load(dir_name + "/" + load_dir_2)
r3 = torch.load(dir_name + "/" + load_dir_3)
#r4 = torch.load(dir_name + "/" + load_dir_4)
#r5 = torch.load(dir_name + "/" + load_dir_5)

for i in range(len(changing_variable)):
    r1[i] = r1[i][0:n_step]
    r2[i] = r2[i][0:n_step]
    r3[i] = r3[i][0:n_step]
#    r4[i] = r4[i][0:n_step]
#    r5[i] = r5[i][0:n_step]

r1 = r1[0:len(changing_variable)]
r2 = r2[0:len(changing_variable)]
r3 = r3[0:len(changing_variable)]
#r4 = r4[0:len(changing_variable)]
#r5 = r5[0:len(changing_variable)]

rewards = [[0. for j in range(len(r1[0]))] for i in range(len(r1))]

rew_ind_avg = []
for j in range(len(changing_variable)):
    for i in range(len(r1[0])):
        rewards[j][i] = r1[j][i] + r2[j][i] + r3[j][i]# + r4[j][i] + r5[j][i]
        rewards[j][i] = rewards[j][i]/3#5

rewards = np.array(rewards)

#rew_ind_total = np.array([r1, r2, r3, r4, r5])
rew_ind_total = np.array([r1, r2, r3])

rew_ind_avg = np.sum(rew_ind_total, axis=1)/len(rewards)

rew_std = np.std(rew_ind_avg, axis=0)

x = [i for i in range(no_steps//1000)]
reward_avg = np.sum(rewards, axis=0)/len(rewards)



fig, ax = plt.subplots(1, 1, figsize=(20, 10))
plt.plot(x, reward_avg, linewidth=5)
plt.fill_between(x, reward_avg + rew_std, reward_avg - rew_std, alpha = 0.1)


plt.xlabel('No of steps X1000')
plt.ylabel("Reward")
plt.title("For SAC trained at " + str(changing_variable_name) + " of " + str(changing_variable[0]) + " averaged over different time stamps")
name = dir_name + "/" + changing_variable_name
plt.savefig(name)
plt.close(fig)