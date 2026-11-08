import re

def compress_system_prompt(prompt_text):
    """
    Compresses a system prompt by removing unnecessary whitespace, 
    newlines, and low-information filler words.
    """
    #Remove multiple spaces, tabs, and newlines
    compressed = re.sub(r'\s+', ' ', prompt_text).strip()
    
    #Define low-information filler words often found in prompts
    with open("data/fluff_words.txt", "r") as f:
        fluff_words = set(f.read().split())
    #Filter out the fluff words (case-insensitive)
    words = compressed.split()
    filtered_words = []
    
    for word in words:
        # Strip basic punctuation to check the word, but keep it in the output
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        if clean_word not in fluff_words:
            filtered_words.append(word)
            
    return " ".join(filtered_words)

#Test
if __name__ == "__main__":
    original_prompt = """
    You are a very helpful AI assistant. Please kindly answer the user's question 
    using only the provided context. It is extremely important that you format 
    the final output as a JSON object.
    """
    
    compressed_prompt = compress_system_prompt(original_prompt)
    
    print("--- Original ---")
    print(original_prompt.strip())
    print(f"Length: {len(original_prompt)} chars\n")
    
    print("--- Compressed ---")
    print(compressed_prompt)
    print(f"Length: {len(compressed_prompt)} chars")
    print(f"Reduction: {100 - (len(compressed_prompt) / len(original_prompt) * 100):.1f}%")