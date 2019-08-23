# Import the necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np

### https://www.datacamp.com/community/tutorials/matplotlib-tutorial-python

# Prepare the data
x = np.linspace(0, 10, 100)

# Plot the data
plt.plot(x, x, label='linear')

# Add a legend
plt.legend()

# Show the plot
plt.show()