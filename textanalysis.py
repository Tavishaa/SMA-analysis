# Import necessary libraries
import nltk
from nltk import FreqDist, word_tokenize, sent_tokenize
import matplotlib.pyplot as plt

# Step 1: Download necessary NLTK data (if not already downloaded)
nltk.download('punkt')

# Step 2: Load your text data from a file (ensure the file is in the same directory as this script)
with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Step 3: Tokenize the text into words and sentences
words = word_tokenize(text)
sentences = sent_tokenize(text)

# ---- Static Text Analysis ----
# Step 4: Compute the overall frequency distribution of words
freq_dist = FreqDist(words)

# Print the 20 most common words to the terminal
print("Top 20 most common words:")
for word, count in freq_dist.most_common(20):
    print(f"{word}: {count}")

# Step 5: Visualize the top 20 words using a bar plot
plt.figure(figsize=(10, 6))
freq_dist.plot(20, title="Top 20 Word Frequencies (Static Analysis)")
plt.savefig("static_analysis.png")  # Save the plot as an image file
plt.show()

# ---- Dynamic Text Analysis ----
# In this example, we analyze how the frequency of a target word changes across the text.
# Step 6: Divide the text into segments (e.g., segments of 50 sentences each)
segment_size = 50  # You can adjust this value
num_sentences = len(sentences)
segments = [sentences[i:i + segment_size] for i in range(0, num_sentences, segment_size)]

# Choose a target word to track (example: 'the')
target_word = "the"
dynamic_freq = []

# Step 7: For each segment, calculate the frequency of the target word
for idx, segment in enumerate(segments, 1):
    segment_text = " ".join(segment)
    segment_words = word_tokenize(segment_text)
    count = segment_words.count(target_word)
    dynamic_freq.append(count)
    print(f"Segment {idx}: Frequency of '{target_word}' = {count}")

# Step 8: Plot the frequency of the target word over the segments
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(dynamic_freq) + 1), dynamic_freq, marker='o', linestyle='-', color='b')
plt.xlabel("Segment Number")
plt.ylabel(f"Frequency of '{target_word}'")
plt.title(f"Dynamic Analysis: Frequency of '{target_word}' Over Text Segments")
plt.grid(True)
plt.savefig("dynamic_analysis.png")  # Save the dynamic analysis plot as an image file
plt.show()
