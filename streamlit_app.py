import streamlit as st
import unicodedata
import re

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
st.title("Word Search App")

# Input for words to search (comma-separated)
words_input = st.text_area("Words to search (comma-separated):", height=100)

# Input for the text to search in
text_to_search = st.text_area("Text to search in:", height=200)

# Search button
if st.button("Search"):
    if words_input and text_to_search:
        # Split words by comma
        words_to_search = [word.strip() for word in words_input.split(',')]
        
        # Run the search function
        result = search_words(text_to_search, words_to_search)

        # Display the results
        st.subheader("Results")
        for word, count in result.items():
            st.write(f"{word}: {count} occurrence(s)")
    else:
        st.error("Please provide both the words and text to search.")
