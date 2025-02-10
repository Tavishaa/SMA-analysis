import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Load hyperlink data
hyperlinks = pd.read_csv('wikipedia_hyperlinks.csv')

# Create a directed graph
G = nx.DiGraph()
for index, row in hyperlinks.iterrows():
    G.add_edge(row['source'], row['target'])

# Compute PageRank (measures influence of Wikipedia pages)
pagerank = nx.pagerank(G)
print("Top 10 Most Influential Wikipedia Pages:")
for page, rank in sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(page)
    print(rank)
    print("------------------")

# Network visualization
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=0.15)
nx.draw(G, pos, with_labels=False, node_size=500, node_color="lightblue", edge_color="gray", font_size=10, font_weight='bold')

central_node = max(pagerank, key=pagerank.get)
nx.draw_networkx_labels(G, pos, labels={central_node: central_node}, font_size=12, font_weight='bold', font_color='black')

plt.title("Wikipedia Hyperlink Network Structure", fontsize=14, fontweight='bold')
plt.savefig("static_hyperlink.png") 
plt.show()