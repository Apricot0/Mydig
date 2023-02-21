import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

fin = input("Enter data input: ")
# Read data from the provided CSV
df = pd.read_csv(fin)

# Create the box plot
sns.boxplot(x='website', y='query_time(ms)', hue='query_method', data=df, showmeans=True, meanline=True, showbox=True, showcaps=True, showfliers=True,meanprops={'color':'black'})

# Show the plot
plt.title("Query time by website and method")
plt.savefig('boxplot.png', dpi=300, bbox_inches='tight')