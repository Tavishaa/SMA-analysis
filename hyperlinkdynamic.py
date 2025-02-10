import networkx as nx
import matplotlib.pyplot as plt

# Function to update network over time
def update_network(graph, new_links):
    for src, tgt in new_links:
        graph.add_edge(src, tgt)
    return graph

# Ensure 'G' is defined before adding new links
if 'G' not in globals():
    G = nx.DiGraph()

# Simulating new links being added dynamically
new_links = [("https://en.wikipedia.org/wiki/Web_scraping", "https://en.wikipedia.org/wiki/Data_scraping"),
             ("https://en.wikipedia.org/wiki/Web_scraping", "https://en.wikipedia.org/wiki/Web_crawler")]
G = update_network(G, new_links)

# Recompute PageRank dynamically
pagerank_updated = nx.pagerank(G)
print("Updated Top 10 Most Influential Wikipedia Pages:")
for page, rank in sorted(pagerank_updated.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(page, "\n", rank, "\n------------------")

# Improved Graph Visualization
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=0.3)  # Adjust k for better spacing
nx.draw(G, pos, with_labels=False, node_size=500, node_color="lightcoral", edge_color="gray", alpha=0.6)

# Label only the central node in the updated graph
central_node_updated = max(pagerank_updated, key=pagerank_updated.get)
nx.draw_networkx_labels(G, pos, labels={central_node_updated: central_node_updated}, 
                        font_size=10, font_weight='bold', font_color='red', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

plt.title("Updated Wikipedia Hyperlink Network Structure", fontsize=14, fontweight='bold')
plt.savefig("dynamic_hyperlink.png", bbox_inches="tight")  # Save graph properly
plt.show()
