import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


FREQ1 = 36e6  # 36MHz
FREQ2 = 48e6  # 48MHz
SAMP_RATE = 480e6  # fs >= f, since fmax is 48
DUR = 1e-6  # 1sec DUR
NUM_SAMP = int(DUR * SAMP_RATE)


t = np.linspace(0, DUR, NUM_SAMP, endpoint=False)

clock_pulse1 = signal.square(2 * np.pi * FREQ1 * t)
clock_pulse2 = signal.square(2 * np.pi * FREQ2 * t)

# plotting
fig, axs = plt.subplots(1, 2, figsize=(12, 4))

axs[0].plot(t, clock_pulse1, color="blue", linewidth=2)
axs[0].set_title("Clock Pulse (Frequency: 36 MHz)")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].set_ylim(-1.2, 1.2)
axs[0].grid(True)

axs[1].plot(t, clock_pulse2, color="blue", linewidth=2)
axs[1].set_title("Clock Pulse (Frequency: 48 MHz)")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].set_ylim(-1.2, 1.2)
axs[1].grid(True)

plt.tight_layout()
plt.show()
