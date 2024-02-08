import numpy as np
import matplotlib.pyplot as plt

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot the data
plt.plot(x, y, label='Sine Wave')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Simple Plot')
plt.legend()
plt.show()

