import numpy as np
from util.new_replay_buffers.task_relevance.replay_buffer import Replay_Memory_TR
from util.new_replay_buffers.task_relevance.gradual_task_with_relevance.custom_res import  Custom_Res_TR
import random
from itertools import count

class Transition_tuple():

    def __init__(self, state, action, action_mean, reward, next_state, done_mask, t, initial_state, time_step):
        #expects as list of items for each initalization variable
        self.state = np.array(state)
        self.action = np.array(action)
        self.action_mean = np.array(action_mean)
        self.reward = np.array(reward)
        self.next_state = np.array(next_state)
        self.done_mask = np.array(done_mask)
        self.t = np.array(t)
        self.initial_state = np.array(initial_state)
        self.time_step = np.array(time_step)

    def get_all_attributes(self):
        return [self.state, self.action,  self.action_mean, self.reward, self.next_state, self.done_mask, self.t, self.initial_state, self.time_step]

class Custom_HRF_TR():

    def __init__(self, capacity=10000, curisoity_buff_frac = 0.34, seperate_cur_buffer=True,
                 fifo_fac = 0.05, avg_len_snr=600, repetition_threshold=30000, snr_factor=2.5, change_at = [100000, 350000]):
        assert (fifo_fac > 0) and (fifo_fac < 1)
        self.fifo_frac = fifo_fac
        self.fifo_capacity = int(capacity*fifo_fac)
        self.reservior_capacity = capacity - self.fifo_capacity

        self.fifo_buffer = Replay_Memory_TR(capacity=self.fifo_capacity)
        self.reservior_buffer = Custom_Res_TR(capacity=self.reservior_capacity,
                                                                     avg_len_snr=avg_len_snr, repetition_threshold=repetition_threshold,
                                                                     snr_factor=snr_factor, change_at=change_at
                                                                     )

        self.t = 0
        self.split_sizes = [0]

    def task_changed_at_current_time_step(self):
        return self.reservior_buffer.task_change_at_current_time_step

    def new_partition(self, buffer):
        self.reservior_buffer.partition_buffer()
        self.consolidate_fifo(buffer.fifo_buffer)
        self.consolidate_reservoir(buffer.reservior_buffer)

    def no_new_partion(self, buffer):
        self.consolidate_fifo(buffer.fifo_buffer)
        self.consolidate_reservoir(buffer.reservior_buffer)

    def consolidate_fifo(self, fifo_buffer):

        print("consolidating fifo buffer")

        for d in fifo_buffer.storage:
            state, action, action_mean, reward, curiosity, next_state, done_mask, initial_state, time_step = d
            self.fifo_buffer.push(state, action, action_mean, reward, next_state, done_mask, initial_state,
                                  time_step)

        print("fifo buffer consolidated")


    def consolidate_reservoir(self, reservoir):
        self.reservior_buffer.consolidate_on_last_partition(reservoir)



    def push(self, state, action, action_mean, reward, next_state, done_mask, initial_state, time_step):
        self.t += 1

        old_data = self.fifo_buffer.push(state, action, action_mean, reward, next_state, done_mask, initial_state, time_step)
        if old_data != None:
            state, action, action_mean, reward, next_state, done_mask, initial_state, time_step = old_data
            self.reservior_buffer.push(state, action, action_mean, reward, next_state, done_mask, None, initial_state, time_step)



    def sample(self, batch_size):
        fifo_indices, reservoir_indices = self.get_sample_indices(batch_size)
        state, action, action_mean, reward, next_state, done_mask, initial_state, time_step = self.encode_sample(fifo_indices, reservoir_indices)

        fifo_batch_size = int(batch_size * self.fifo_frac)
        self.reservior_buffer.split_sizes.append(fifo_batch_size)
        self.split_sizes = self.reservior_buffer.split_sizes


        return Transition_tuple(state, action, action_mean, reward, next_state, done_mask,None, initial_state, time_step)



    def encode_sample(self, fifo_indices, reservior_indices):

        state, action, action_mean, reward,  next_state, done_mask, initial_state, time_step = [], [], [], [], [], [], [], []
        s1, a1, a_m1, r1, n_s1, d1, i_s1, t_s1 = self.fifo_buffer.encode_sample(fifo_indices)
        s2, a2, a_m2, r2, n_s2, d2, t2, i_s2, t_s2 = self.reservior_buffer.encode_sample(reservior_indices)


        state = state + s1 + s2
        action = action + a1 + a2
        action_mean = action_mean + a_m1 + a_m2
        reward = reward + r1 + r2
        next_state = next_state + n_s1 + n_s2
        done_mask = done_mask + d1 + d2
        initial_state = i_s1 + i_s2
        time_step = t_s1 + t_s2


        return state, action, action_mean, reward, next_state, done_mask, initial_state, time_step

    def get_sample_indices(self, batch_size):


        fifo_batch_size = int(batch_size * self.fifo_frac)
        reservoir_batch_size = batch_size - fifo_batch_size

        if len(self.reservior_buffer) < reservoir_batch_size:
            reservoir_batch_size = len(self.reservior_buffer)
            fifo_batch_size = batch_size - reservoir_batch_size



        fifo_indices = self.fifo_buffer.get_sample_indices(fifo_batch_size)
        reservoir_indices = self.reservior_buffer.get_sample_indices(reservoir_batch_size)

        return fifo_indices, reservoir_indices


    def __len__(self):
        return len(self.fifo_buffer) + len(self.reservior_buffer)