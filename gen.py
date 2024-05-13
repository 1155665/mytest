import numpy as np

class SineWaveGenerator:
    def __init__(self, amplitude, frequency, phase):
        """
        Initialize the SineWaveGenerator class.

        Parameters:
        amplitude (float): The amplitude of the sine wave.
        frequency (float): The frequency of the sine wave.
        phase (float): The phase of the sine wave.
        """
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def generate_signal(self, duration, sample_rate):
        """
        Generate a sine wave signal.

        Parameters:
        duration (float): The duration of the signal in seconds.
        sample_rate (int): The sample rate of the signal in samples per second.

        Returns:
        numpy.ndarray: The generated sine wave signal.
        """
        time = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * time + self.phase)
        return signal
        