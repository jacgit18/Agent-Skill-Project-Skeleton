#!/usr/bin/env python3
"""
Simple AI QA Tool: Prompt Consistency & Output Validator

This is a minimal example of Pattern 1 (Consistency Testing) + Pattern 2 (Format Validation).
It validates that a prompt produces consistent and well-formatted outputs.
"""

import json
import re
from typing import List, Dict

def validate_prompt_consistency(
    prompt: str,
    test_inputs: List[str],
    run_count: int = 3,
    simulate_llm: bool = True
) -> Dict:
    """
    Validate that a prompt produces consistent outputs across multiple runs.
    
    In real use, this would call an LLM (Claude, GPT, etc.) multiple times.
    For demo, we simulate with mock outputs.
    """
    
    print(f"Testing prompt consistency: {run_count} runs × {len(test_inputs)} inputs")
    
    consistency_scores = []
    
    for test_input in test_inputs:
        outputs = []
        
        for run in range(run_count):
            # In real usage: output = call_llm(prompt, test_input)
            # For demo: simulate output
            if simulate_llm:
                # Mock: category output varies slightly (simulating LLM variance)
                categories = ["groceries", "dining", "transportation", "utilities"]
                import random
                category = categories[random.randint(0, 3)]
                output = f"Category: {category}"
            else:
                output = "You would call your LLM here"
            
            outputs.append(output)
        
        # Measure consistency (simple: how many runs agree on first output)
        if len(set(outputs)) == 1:
            consistency = 1.0  # Perfect consistency
        else:
            consistency = len([o for o in outputs if o == outputs[0]]) / run_count
        
        consistency_scores.append(consistency)
        print(f"  Input: '{test_input}' → consistency: {consistency:.0%}")
    
    avg_consistency = sum(consistency_scores) / len(consistency_scores)
    return {
        "avg_consistency": avg_consistency,
        "status": "PASS" if avg_consistency > 0.8 else "FAIL"
    }

def validate_output_format(
    output: str,
    format_type: str = "json"
) -> Dict:
    """
    Validate that output matches expected format.
    """
    
    if format_type == "json":
        try:
            json.loads(output)
            return {"valid": True, "format": "json"}
        except json.JSONDecodeError:
            return {"valid": False, "format": "json", "error": "Invalid JSON"}
    
    elif format_type == "csv":
        # Simple CSV validation: rows separated by newline, fields by comma
        lines = output.strip().split('\n')
        if len(lines) > 0 and ',' in lines[0]:
            return {"valid": True, "format": "csv", "rows": len(lines)}
        else:
            return {"valid": False, "format": "csv", "error": "Not valid CSV"}
    
    else:
        return {"valid": True, "format": "unknown"}

# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("AI QA Testing Demo: Simple Prompt Validator")
    print("=" * 60)
    
    # Test 1: Consistency
    print("\n[Test 1] Prompt Consistency Testing")
    prompt = "Categorize this expense: {transaction}"
    test_inputs = [
        "Whole Foods, $45",
        "Uber, $12",
        "Coffee shop, $6"
    ]
    
    result = validate_prompt_consistency(prompt, test_inputs, run_count=3)
    print(f"Result: {result['status']} (consistency: {result['avg_consistency']:.0%})\n")
    
    # Test 2: Format validation
    print("[Test 2] Output Format Validation")
    
    json_output = '{"category": "groceries", "confidence": 0.95}'
    csv_output = "Date,Amount,Category\n2026-08-30,45.00,groceries"
    bad_json = '{"incomplete": '
    
    print(f"  JSON valid: {validate_output_format(json_output, 'json')['valid']}")
    print(f"  CSV valid: {validate_output_format(csv_output, 'csv')['valid']}")
    print(f"  Bad JSON valid: {validate_output_format(bad_json, 'json')['valid']}\n")
    
    print("=" * 60)
    print("Demo complete. These are the building blocks for AI QA testing.")
    print("Next: Integrate with promptfoo for production-scale evaluation.")
