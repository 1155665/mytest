# -*- coding: utf-8 -*-

import numpy as np

class SinSignalx(object):
    """A class representing a sinusoidal signal with noise.

    Parameters
    ----------
    freq : float
        The frequency of the signal.
    
    signal_amp : float
        The amplitude of the signal.

    noise_amp : float
        The amplitude of the noise.

    Attributes
    ----------
    sn : int
        The number of samples.
    
    s : numpy.ndarray
        The signal with noise.
    
    pointer : int
        The current pointer position in the signal.

    Methods
    -------
    __init__(freq, signal_amp, noise_amp)
        Initializes the SinSignalx object.
    
    __add__(o)
        Adds the signal of another SinSignalx object to the current signal.
    
    get_data_points(n)
        Returns the next n data points from the signal.

    """

    def __init__(self, freq, signal_amp, noise_amp):
        super(SinSignalx, self).__init__()
        self.sn = 128  # sample number
        t = np.linspace(0, 1, self.sn, endpoint=False)
        u = np.sin(2 * np.pi * freq * t) * signal_amp
        n = np.random.rand(self.sn) * noise_amp
        self.s = u + n
        self.pointer = 0

    def __add__(self, o):
        self.s = self.s + o.s
        return self

    def get_data_points(self, n):
        """Returns the next n data points from the signal.

        Parameters
        ----------
        n : int
            The number of data points to retrieve.

        Returns
        -------
        numpy.ndarray
            The next n data points from the signal.

        """
        next_idx = self.pointer + n
        if next_idx >= self.sn:
            remainder_n = next_idx - self.sn
            tmp = self.s[self.pointer:]
            tmp2 = self.s[:remainder_n]
            self.pointer = remainder_n
            return np.concatenate((tmp, tmp2), axis=0)
        else:
            tmp = self.s[self.pointer:next_idx]
            self.pointer = next_idx
            return tmp

