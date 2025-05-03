import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create the figure
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Initial boat position
boat, = ax.plot([4, 5, 6], [6, 8, 6], 'brown')

def update(frame):
    # Simulate sinking by shifting the boat down
    boat.set_ydata([6, 8, 6] - frame * 0.1)
    return boat,

# Animation
ani = FuncAnimation(fig, update, frames=50, interval=100)
plt.show()
