
import pandas as pd

# Create a DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 34, 29, 32],
        'City': ['New York', 'Paris', 'Berlin', 'London']}
df = pd.DataFrame(data)

# Filter rows where Age > 30
older_than_30 = df[df['Age'] > 30]

print(df)
print(older_than_30)
