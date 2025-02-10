import nltk
from nltk import FreqDist, word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
import string

nltk.download('punkt')
nltk.download('stopwords')

file_path = r"C:/Users/91702/OneDrive\Desktop\SMA\ALice's_Adventure_In_The_Wonderland.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()


words = word_tokenize(text)
sentences = sent_tokenize(text)

words = [word.lower() for word in words if word.isalnum()]

stop_words = set(nltk.corpus.stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]

# ---- Static Text Analysis ----

# Compute the overall frequency distribution of words
freq_dist = FreqDist(filtered_words)

# Print the 20 most common words
print("Top 20 most common words:")
for word, count in freq_dist.most_common(20):
    print(f"{word}: {count}")

# Visualize the top 20 words
plt.figure(figsize=(10, 6))
freq_dist.plot(20, title="Top 20 Word Frequencies (Static Analysis)")
plt.savefig("static_analysis.png")
plt.show()

# ---- Dynamic Text Analysis ----

# Analyze how a target word changes across the text
segment_size = 50 
num_sentences = len(sentences)
segments = [sentences[i:i + segment_size] for i in range(0, num_sentences, segment_size)]

# Choose a target word to track
target_word = "alice"  
dynamic_freq = []

# Calculate the frequency of the target word in each segment
for idx, segment in enumerate(segments, 1):
    segment_text = " ".join(segment)
    segment_words = word_tokenize(segment_text)
    segment_words = [word.lower() for word in segment_words if word.isalnum()]  # Clean words
    count = segment_words.count(target_word)
    dynamic_freq.append(count)
    print(f"Segment {idx}: Frequency of '{target_word}' = {count}")

# Plot the frequency of the target word over segments
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(dynamic_freq) + 1), dynamic_freq, marker='o', linestyle='-', color='b')
plt.xlabel("Segment Number")
plt.ylabel(f"Frequency of '{target_word}'")
plt.title(f"Dynamic Analysis: Frequency of '{target_word}' Over Text Segments")
plt.grid(True)
plt.savefig("dynamic_analysis.png")
plt.show()
