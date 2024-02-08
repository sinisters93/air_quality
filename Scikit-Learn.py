from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression

# Generate regression dataset
X, y = make_regression(n_samples=100, n_features=1, noise=0.1)

# Split dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the values
predictions = model.predict(X_test)
print(f"Predictions: {predictions}")
