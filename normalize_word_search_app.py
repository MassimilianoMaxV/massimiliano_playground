import streamlit as st
import unicodedata
import re
from collections import OrderedDict

# Function to normalize text (from the provided code)
def normalize_text(text):
    """
    Normalize the text by converting to lowercase, removing accents, special characters, and spaces.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # Remove special characters and spaces
    text = re.sub(r'[^a-z0-9]', '', text)

    return text

# Function to highlight the words in the text (even across line breaks)
def highlight_words(text, words):
    """
    Highlight words in the text by wrapping them in a span with a red color style.
    Handles words that are split across lines.
    """
    # Join the text by removing line breaks but keeping their positions
    original_lines = text.splitlines()  # Split by line to preserve structure
    joined_text = ''.join(original_lines)  # Join lines for word matching

    # Highlight words in the joined text
    for word in words:
        word_pattern = r'\b' + re.escape(word) + r'\b'  # Escape special characters and add word boundaries
        # Highlight words case-insensitively in the joined text
        joined_text = re.sub(word_pattern, r'<span style="color:red">\g<0></span>', joined_text, flags=re.IGNORECASE)

    # After highlighting, restore the original line breaks
    highlighted_text_with_breaks = re.sub(r'(<span.*?>)([^<]*?)(</span>)', lambda m: m.group(1) + ''.join(f'{part}\n' for part in m.group(2).split('\n')) + m.group(3), joined_text)

    return highlighted_text_with_breaks

# Function to search words in the text (from the provided code)
def search_words(text, words):
    """
    Search for words in the normalized text.
    """
    # Normalize the text
    normalized_text = normalize_text(text)

    # Normalize the words to search for
    normalized_words = [normalize_text(word) for word in words]

    # Initialize a dictionary to store the count of each word
    word_counts = {word: 0 for word in normalized_words}

    # Search for each word in the normalized text
    for word in normalized_words:
        # Use string count method to find all occurrences of the word
        count = normalized_text.count(word)
        word_counts[word] = count

    return word_counts

# Streamlit App Layout
st.title("Normalize Word Search")

# Input for words to search (comma-separated)
words_input = st.text_area("Words to search (comma-separated) - Mots a chercher (séparés par la virgule):", height=100)

# Input for the text to search in
text_to_search = st.text_area("Text to search in title or description - Texte à chercher dans le titre ou description:", height=200)

# Search button
if st.button("Search"):
    if words_input and text_to_search:
        # Split words by comma
        words_to_search = [word.strip() for word in words_input.split(',')]

        # Run the search function
        result = search_words(text_to_search, words_to_search)

        # Highlight the words in the text (without normalizing for highlighting)
        highlighted_text = highlight_words(text_to_search, words_to_search)

        # Sort the results based on the number of occurrences and alphabetical order
        sorted_result = OrderedDict(sorted(result.items(), key=lambda x: (-x[1], x[0])))

        # Display the results
        st.subheader("Results")
        for word, count in sorted_result.items():
            if count > 0:
                st.write(f"<span style='color:green;font-weight:bold'>{word}: {count} occurrence(s)</span>", unsafe_allow_html=True)
            else:
                st.write(f"{word}: {count} occurrence(s)")
    else:
        st.error("Please provide both the words and text to search.")
