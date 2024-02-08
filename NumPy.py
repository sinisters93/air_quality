
import numpy as np

# Create a 2D array of shape (3, 4)
array_2d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# Calculate the transpose
transpose_array = array_2d.T

# Compute the mean of each column
mean_col = np.mean(array_2d, axis=0)

print(f"Original Array:\n{array_2d}")
print(f"Transpose:\n{transpose_array}")
print(f"Mean of each column:\n{mean_col}")
