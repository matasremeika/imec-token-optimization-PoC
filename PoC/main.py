import re
from similarity import calculate_similarity_score
from compress import compress_system_prompt

#Read inputs
with open("data/context.txt", "r") as f:
    raw_context = f.read()

with open("data/query.txt", "r") as f:
    user_query = f.read().strip()

with open("data/system_prompt.txt", "r") as f:
    raw_system_prompt = f.read().strip()

#Chunking: Split documents into smaller, scorable units (sentences)
def chunk_document(text):
    """Splits raw text into sentences using basic regex."""
    # Matches punctuation followed by a space
    sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
    return [s.strip() for s in sentences if len(s) > 10] # Filter out tiny artifacts

#Pruning: Filter and keep only the most relevant chunks
def prune_context(query, documents, top_k=3, threshold=0.15):
    """Scores chunks and returns the top K sentences above a certain threshold."""
    scored_chunks = []
    
    for doc in documents:
        sentences = chunk_document(doc)
        for sentence in sentences:
            score = calculate_similarity_score(query, sentence)
            if score >= threshold:
                scored_chunks.append((score, sentence))
                
    # Sort by score descending
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    
    # Return just the text of the top K chunks
    return [chunk for score, chunk in scored_chunks[:top_k]]

# --- Experiment Execution ---

if __name__ == "__main__":
    #Optimize the system prompt
    optimized_system_prompt = compress_system_prompt(raw_system_prompt)
    
    #Run the pruning algorithm
    pruned_chunks = prune_context(user_query, [raw_context], top_k=2)
    optimized_context = " ".join(pruned_chunks)
    
    #Assemble BOTH prompts for comparison
    baseline_prompt = f"""System: {raw_system_prompt}
Context: {raw_context}
Question: {user_query}"""

    optimized_prompt = f"""System: {optimized_system_prompt}
Context: {optimized_context}
Question: {user_query}"""

    #Print the visual comparison
    print("=========================================")
    print("           BASELINE PROMPT               ")
    print("=========================================")
    print(baseline_prompt)
    
    print("\n=========================================")
    print("          OPTIMIZED PROMPT               ")
    print("=========================================")
    print(optimized_prompt)
    
    #Metric Tracking (Total Payload)
    original_char_count = len(baseline_prompt)
    optimized_char_count = len(optimized_prompt)
    
    print(f"\n--- Metrics ---")
    print(f"Original Total Length:  {original_char_count} characters")
    print(f"Optimized Total Length: {optimized_char_count} characters")
    
    if original_char_count > 0:
        reduction = 100 - (optimized_char_count / original_char_count * 100)
        print(f"Total Token Reduction:  {reduction:.1f}%")
#Additional Simulated Metrics
    # Assuming the LLM processes 15,000 characters per second (Prefill rate)
    CHARS_PER_SECOND = 15000 
    # Assume it costs $0.50 per 1 million input characters
    COST_PER_1M_CHARS = 0.50 

    baseline_latency = original_char_count / CHARS_PER_SECOND
    optimized_latency = optimized_char_count / CHARS_PER_SECOND

    baseline_cost = (original_char_count / 1_000_000) * COST_PER_1M_CHARS
    optimized_cost = (optimized_char_count / 1_000_000) * COST_PER_1M_CHARS

    print(f"\n--- Simulated Business Impact ---")
    print(f"Baseline Latency (TTFT):  {baseline_latency:.4f} seconds")
    print(f"Optimized Latency (TTFT): {optimized_latency:.4f} seconds")
    print(f"Latency Saved per call:   {baseline_latency - optimized_latency:.4f} seconds")
    print(f"Cost per 10k requests (Baseline):  ${(baseline_cost * 10000):.2f}")
    print(f"Cost per 10k requests (Optimized): ${(optimized_cost * 10000):.2f}")