from util.reservoir_w_cur_replay_buffer import Reservoir_with_Cur_Replay_Memory

#from moving_average import n_c, avg_len
from additional_test.Test_Filters.filter_stuff.winer import n_a_c as n_c

mul = 1000
change_var_at = [0, 100, 150, 350]
change_var_at = [change_var_at[i]*mul for i in range(len(change_var_at))]

M = Reservoir_with_Cur_Replay_Memory(50000)



for c in n_c:
   M.push(0,0,0,0,c,0,0)

x1 = 0
x2 = 0
x3 = 0
x4 = 0
a = M.storage
for i in range(len(a)):
    if a[i][1] >= change_var_at[0] and a[i][1] < change_var_at[1]:
        x1 += 1
    elif a[i][1] >= change_var_at[1] and a[i][1] < change_var_at[2]:
        x2 += 1
    elif a[i][1] >= change_var_at[2] and a[i][1] < change_var_at[3]:
        x3 += 1
    elif a[i][1] >= change_var_at[3]:
        x4 += 1




print(x1, x2, x3, x4)
size = len(a)
data = [x1/size, x2/size, x3/size, x4/size]
print(data)
print(len(M))


