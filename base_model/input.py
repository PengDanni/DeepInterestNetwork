import numpy as np


class DataInput:
    def __init__(self, data, batch_size):

        # number of samples in one batch
        self.batch_size = batch_size
        self.data = data
        # number of batches in one epoch
        self.epoch_size = len(self.data) // self.batch_size  # // operator floor
        if self.epoch_size * self.batch_size < len(self.data):  # operator ceiling
            self.epoch_size += 1
        # current batch number
        self.i = 0

    def __iter__(self):
        return self

    def next(self):

        if self.i == self.epoch_size:
            raise StopIteration

        ts = self.data[self.i * self.batch_size: min((self.i + 1) * self.batch_size,
                                                     len(self.data))]  # retrieve train samples for current batch
        self.i += 1

        u, i, y, sl = [], [], [], []
        for t in ts:
            u.append(t[0])  # user
            i.append(t[2])  # item (including positive and negative samples)
            y.append(t[3])  # label
            sl.append(len(t[1]))  # shopping history length / sequence length
        max_sl = max(sl)

        hist_i = np.zeros([len(ts), max_sl], np.int64)  # create a 0 padded numpy matrix of shape(ts_size, max_hist_len)

        k = 0  # track the sample index
        for t in ts:
            for l in range(len(t[1])):
                hist_i[k][l] = t[1][l]  # convert list of history lists into a matrix
            k += 1

        return self.i, (u, i, y, hist_i, sl)


class DataInputTest:
    """data input for test after one batch training???"""
    def __init__(self, data, batch_size):

        self.batch_size = batch_size
        self.data = data
        self.epoch_size = len(self.data) // self.batch_size
        if self.epoch_size * self.batch_size < len(self.data):
            self.epoch_size += 1
        self.i = 0

    def __iter__(self):
        return self

    def next(self):

        if self.i == self.epoch_size:
            raise StopIteration

        ts = self.data[self.i * self.batch_size: min((self.i + 1) * self.batch_size,
                                                     len(self.data))]
        self.i += 1

        u, i, j, sl = [], [], [], []
        for t in ts:
            u.append(t[0])
            i.append(t[2][0])  # positive item
            j.append(t[2][1])  # negative item
            sl.append(len(t[1]))
        max_sl = max(sl)

        hist_i = np.zeros([len(ts), max_sl], np.int64)

        k = 0
        for t in ts:
            for l in range(len(t[1])):
                hist_i[k][l] = t[1][l]
            k += 1

        return self.i, (u, i, j, hist_i, sl)
