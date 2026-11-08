# Token Optimization Proof of Concept (PoC)

This repository contains a Proof of Concept (PoC) demonstrating input token optimization strategies for an LLM-based operational knowledge assistant. 

The primary goal of this codebase is to reduce API costs and prefill latency (Time-to-First-Token) without compromising the accuracy of the LLM's response.

## Optimization Techniques Implemented

1. **Context Pruning (Dynamic Thresholding):** Utilizes the Levenshtein distance algorithm to calculate lexical similarity between a user query and chunked document sentences, isolating and retaining only the most relevant context.
2. **System Prompt Compression:** A lexical filter that strips low-information "fluff" words from the static system instructions, heavily reducing the baseline token footprint per request.

## Project Structure

```text
PoC/
│
├── main.py              # Main execution script and metric calculator
├── similarity.py        # Levenshtein distance algorithm implementation
├── compress.py          # Prompt compression logic and lexical filtering
│
└── data/                # Mock data inputs for the PoC
    ├── context.txt      # Raw knowledge base text
    ├── query.txt        # User query 
    ├── system_prompt.txt # Baseline system instructions
    └── fluff_words.txt  # Dictionary of low-information filler words