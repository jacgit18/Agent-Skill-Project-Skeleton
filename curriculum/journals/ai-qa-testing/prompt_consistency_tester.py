#!/usr/bin/env python3
"""
Prompt Consistency Tester

A simple tool to measure how consistently a prompt produces similar outputs.
This is a foundational AI QA pattern: prompt validation through repetition.

Usage:
    python prompt_consistency_tester.py
"""

import anthropic
import json
from difflib import SequenceMatcher
from typing import Optional


def calculate_string_similarity(str1: str, str2: str) -> float:
    """Calculate string similarity using SequenceMatcher (0.0 to 1.0)."""
    return SequenceMatcher(None, str1, str2).ratio()


def semantic_similarity_via_llm(text1: str, text2: str, client: anthropic.Anthropic) -> float:
    """
    Use Claude to evaluate semantic similarity between two outputs.
    Returns a score from 0.0 to 1.0 where 1.0 = identical meaning.
    """
    prompt = f"""Rate how semantically similar these two texts are (0.0 = completely different, 1.0 = identical meaning).
Respond ONLY with a number between 0.0 and 1.0.

Text 1: {text1}

Text 2: {text2}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        score = float(response.content[0].text.strip())
        return max(0.0, min(1.0, score))  # Clamp to 0.0-1.0
    except (ValueError, AttributeError):
        # If Claude doesn't return a number, default to string similarity
        return calculate_string_similarity(text1, text2)


def run_prompt_consistency_test(
    prompt: str,
    test_input: str,
    num_runs: int = 5,
    temperature: float = 0.7,
    model: str = "claude-haiku-4-5-20251001",
    use_semantic_scoring: bool = True
) -> dict:
    """
    Test prompt consistency by running it multiple times and analyzing output variance.

    Args:
        prompt: The prompt template (use {input} as placeholder)
        test_input: The input to test with
        num_runs: Number of times to run the prompt (default 5)
        temperature: LLM temperature (default 0.7)
        model: Model to use (default haiku for cost)
        use_semantic_scoring: Whether to use LLM-based semantic similarity (slower, more accurate)

    Returns:
        Dictionary with consistency metrics and results
    """
    client = anthropic.Anthropic()

    print(f"\n=== Prompt Consistency Test ===")
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    print(f"Runs: {num_runs}")
    print(f"Semantic scoring: {use_semantic_scoring}\n")

    # Format the prompt with the test input
    formatted_prompt = prompt.format(input=test_input) if "{input}" in prompt else prompt

    outputs = []
    print("Running tests...")

    for i in range(num_runs):
        print(f"  Run {i+1}/{num_runs}...", end=" ", flush=True)
        response = client.messages.create(
            model=model,
            max_tokens=500,
            temperature=temperature,
            messages=[{"role": "user", "content": formatted_prompt}]
        )
        output = response.content[0].text.strip()
        outputs.append(output)
        print(f"({len(output)} chars)")

    # Calculate string similarities
    print("\nCalculating string similarity...")
    string_similarities = []
    for i in range(len(outputs)):
        for j in range(i + 1, len(outputs)):
            sim = calculate_string_similarity(outputs[i], outputs[j])
            string_similarities.append(sim)

    avg_string_similarity = sum(string_similarities) / len(string_similarities) if string_similarities else 0.0

    # Calculate semantic similarities if requested
    semantic_similarities = []
    if use_semantic_scoring and num_runs > 1:
        print("Calculating semantic similarity (this may take a moment)...")
        for i in range(len(outputs)):
            for j in range(i + 1, len(outputs)):
                sim = semantic_similarity_via_llm(outputs[i], outputs[j], client)
                semantic_similarities.append(sim)
        avg_semantic_similarity = sum(semantic_similarities) / len(semantic_similarities)
    else:
        avg_semantic_similarity = None

    # Prepare results
    results = {
        "prompt": prompt,
        "test_input": test_input,
        "num_runs": num_runs,
        "temperature": temperature,
        "model": model,
        "outputs": outputs,
        "metrics": {
            "avg_string_similarity": round(avg_string_similarity, 3),
            "min_string_similarity": round(min(string_similarities), 3) if string_similarities else 0.0,
            "max_string_similarity": round(max(string_similarities), 3) if string_similarities else 1.0,
        }
    }

    if avg_semantic_similarity is not None:
        results["metrics"]["avg_semantic_similarity"] = round(avg_semantic_similarity, 3)
        results["metrics"]["min_semantic_similarity"] = round(min(semantic_similarities), 3) if semantic_similarities else 0.0
        results["metrics"]["max_semantic_similarity"] = round(max(semantic_similarities), 3) if semantic_similarities else 1.0

    # Print results
    print("\n=== Results ===")
    print(f"String Similarity: {results['metrics']['avg_string_similarity']:.1%} (avg)")
    if avg_semantic_similarity is not None:
        print(f"Semantic Similarity: {results['metrics']['avg_semantic_similarity']:.1%} (avg)")

    print("\n=== Sample Outputs ===")
    for i, output in enumerate(outputs[:3]):  # Show first 3
        preview = output[:100] + "..." if len(output) > 100 else output
        print(f"  Run {i+1}: {preview}")

    return results


def test_simple_prompt():
    """Test a simple, well-defined prompt."""
    prompt = "Summarize this in exactly one sentence: {input}"
    test_input = "The sky is blue because light scatters. Most other colors scatter less."

    return run_prompt_consistency_test(
        prompt=prompt,
        test_input=test_input,
        num_runs=3,
        temperature=0.5,  # Lower temp for consistency
        use_semantic_scoring=True
    )


def test_creative_prompt():
    """Test a more creative/variable prompt."""
    prompt = "Write a short, creative product description (1-2 sentences) for: {input}"
    test_input = "A ceramic coffee mug"

    return run_prompt_consistency_test(
        prompt=prompt,
        test_input=test_input,
        num_runs=3,
        temperature=0.9,  # Higher temp for variety
        use_semantic_scoring=True
    )


if __name__ == "__main__":
    print("Starting Prompt Consistency Testing\n")

    # Run example tests
    print("\n" + "="*50)
    print("TEST 1: Well-defined prompt (low temperature)")
    print("="*50)
    results1 = test_simple_prompt()

    print("\n" + "="*50)
    print("TEST 2: Creative prompt (high temperature)")
    print("="*50)
    results2 = test_creative_prompt()

    # Save results
    all_results = {
        "test_1_summary": results1["metrics"],
        "test_2_creative": results2["metrics"],
    }

    with open("consistency_test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "="*50)
    print("Results saved to consistency_test_results.json")
    print("="*50)
