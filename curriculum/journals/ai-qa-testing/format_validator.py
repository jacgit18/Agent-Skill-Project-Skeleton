#!/usr/bin/env python3
"""
Format Validator for AI QA

Validates that AI outputs match expected format specifications.
Implements Pattern 2 from notes: Format Validation.

Supports:
- JSON schema validation
- Regex pattern matching
- Custom validation functions
"""

import json
import re
from typing import Any, Callable, Optional, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    details: dict = None


class FormatValidator:
    """Validates AI-generated outputs against format specifications."""

    @staticmethod
    def validate_json(output: str, required_fields: Optional[List[str]] = None) -> ValidationResult:
        """
        Validate that output is valid JSON with required fields.

        Args:
            output: The string output to validate
            required_fields: List of field names that must be present

        Returns:
            ValidationResult with pass/fail and details
        """
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            return ValidationResult(
                passed=False,
                message=f"Invalid JSON: {str(e)}",
                details={"error": str(e)}
            )

        if not isinstance(data, dict):
            return ValidationResult(
                passed=False,
                message="JSON is not an object (dict)",
                details={"type": type(data).__name__}
            )

        if required_fields:
            missing = [field for field in required_fields if field not in data]
            if missing:
                return ValidationResult(
                    passed=False,
                    message=f"Missing required fields: {missing}",
                    details={"missing_fields": missing, "found_fields": list(data.keys())}
                )

        return ValidationResult(
            passed=True,
            message=f"Valid JSON with {len(data)} fields",
            details={"fields": list(data.keys())}
        )

    @staticmethod
    def validate_json_schema(output: str, schema: dict) -> ValidationResult:
        """
        Validate JSON output against a schema (basic type checking).

        Args:
            output: JSON string to validate
            schema: Dict with field names and expected types, e.g. {"name": str, "age": int}

        Returns:
            ValidationResult
        """
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            return ValidationResult(
                passed=False,
                message=f"Invalid JSON: {str(e)}"
            )

        errors = []
        for field, expected_type in schema.items():
            if field not in data:
                errors.append(f"Missing field: {field}")
            elif not isinstance(data[field], expected_type):
                actual_type = type(data[field]).__name__
                expected_name = expected_type.__name__
                errors.append(f"Field '{field}' has type {actual_type}, expected {expected_name}")

        if errors:
            return ValidationResult(
                passed=False,
                message=f"Schema validation failed: {len(errors)} error(s)",
                details={"errors": errors}
            )

        return ValidationResult(
            passed=True,
            message="All fields match schema",
            details={"validated_fields": len(schema)}
        )

    @staticmethod
    def validate_regex(output: str, pattern: str) -> ValidationResult:
        """
        Validate that output matches a regex pattern.

        Args:
            output: String to validate
            pattern: Regex pattern to match

        Returns:
            ValidationResult
        """
        try:
            compiled = re.compile(pattern)
        except re.error as e:
            return ValidationResult(
                passed=False,
                message=f"Invalid regex pattern: {str(e)}"
            )

        if compiled.search(output):
            return ValidationResult(
                passed=True,
                message=f"Output matches pattern",
                details={"pattern": pattern}
            )
        else:
            return ValidationResult(
                passed=False,
                message=f"Output does not match pattern",
                details={"pattern": pattern, "output_preview": output[:100]}
            )

    @staticmethod
    def validate_length(output: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> ValidationResult:
        """
        Validate output length is within bounds.

        Args:
            output: String to validate
            min_length: Minimum acceptable length
            max_length: Maximum acceptable length

        Returns:
            ValidationResult
        """
        length = len(output)
        errors = []

        if min_length is not None and length < min_length:
            errors.append(f"Too short ({length} < {min_length})")
        if max_length is not None and length > max_length:
            errors.append(f"Too long ({length} > {max_length})")

        if errors:
            return ValidationResult(
                passed=False,
                message=f"Length validation failed: {errors[0]}",
                details={"length": length, "min": min_length, "max": max_length}
            )

        return ValidationResult(
            passed=True,
            message=f"Length valid ({length} chars)",
            details={"length": length}
        )

    @staticmethod
    def validate_contains_keywords(output: str, keywords: List[str]) -> ValidationResult:
        """
        Validate that output contains all required keywords.

        Args:
            output: String to check
            keywords: List of keywords that must appear

        Returns:
            ValidationResult
        """
        output_lower = output.lower()
        missing = [kw for kw in keywords if kw.lower() not in output_lower]

        if missing:
            return ValidationResult(
                passed=False,
                message=f"Missing keywords: {missing}",
                details={"missing": missing, "required": keywords}
            )

        return ValidationResult(
            passed=True,
            message=f"All {len(keywords)} keywords found",
            details={"keywords_found": len(keywords)}
        )

    @staticmethod
    def validate_custom(output: str, validator_fn: Callable[[str], bool], name: str = "custom") -> ValidationResult:
        """
        Validate using a custom validation function.

        Args:
            output: String to validate
            validator_fn: Function that returns True if valid, False otherwise
            name: Name of the validator for error messages

        Returns:
            ValidationResult
        """
        try:
            is_valid = validator_fn(output)
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Validator error: {str(e)}"
            )

        if is_valid:
            return ValidationResult(
                passed=True,
                message=f"Custom validator '{name}' passed"
            )
        else:
            return ValidationResult(
                passed=False,
                message=f"Custom validator '{name}' failed"
            )


class ValidationSuite:
    """Run multiple validators on a single output."""

    def __init__(self):
        self.validators = []

    def add_json_validation(self, required_fields: Optional[List[str]] = None):
        """Add JSON validation."""
        self.validators.append(
            ("JSON format", lambda output: FormatValidator.validate_json(output, required_fields))
        )
        return self

    def add_regex_validation(self, pattern: str, name: str = "regex"):
        """Add regex validation."""
        self.validators.append(
            (name, lambda output, p=pattern: FormatValidator.validate_regex(output, p))
        )
        return self

    def add_length_validation(self, min_length: Optional[int] = None, max_length: Optional[int] = None):
        """Add length validation."""
        self.validators.append(
            ("length", lambda output: FormatValidator.validate_length(output, min_length, max_length))
        )
        return self

    def add_keywords_validation(self, keywords: List[str], name: str = "keywords"):
        """Add keyword validation."""
        self.validators.append(
            (name, lambda output, kw=keywords: FormatValidator.validate_contains_keywords(output, kw))
        )
        return self

    def add_custom_validation(self, validator_fn: Callable[[str], bool], name: str):
        """Add custom validation."""
        self.validators.append(
            (name, lambda output, fn=validator_fn: FormatValidator.validate_custom(output, fn, name))
        )
        return self

    def run(self, output: str) -> tuple[bool, List[dict]]:
        """
        Run all validators on output.

        Returns:
            (all_passed: bool, results: list of ValidationResult dicts)
        """
        results = []
        all_passed = True

        for name, validator_fn in self.validators:
            result = validator_fn(output)
            results.append({
                "name": name,
                "passed": result.passed,
                "message": result.message,
                "details": result.details or {}
            })
            if not result.passed:
                all_passed = False

        return all_passed, results


# Example usage
if __name__ == "__main__":
    print("=== Format Validator Examples ===\n")

    # Example 1: JSON with required fields
    print("Example 1: JSON with required fields")
    print("-" * 40)
    json_output = '{"name": "Alice", "age": 30, "city": "NYC"}'
    result = FormatValidator.validate_json(json_output, required_fields=["name", "age"])
    print(f"Input: {json_output}")
    print(f"Result: {result.passed} - {result.message}\n")

    # Example 2: Invalid JSON
    print("Example 2: Invalid JSON")
    print("-" * 40)
    bad_json = '{"name": "Bob", "age": 25'  # Missing closing brace
    result = FormatValidator.validate_json(bad_json)
    print(f"Input: {bad_json}")
    print(f"Result: {result.passed} - {result.message}\n")

    # Example 3: Validation suite
    print("Example 3: Multi-validator suite")
    print("-" * 40)
    suite = (
        ValidationSuite()
        .add_json_validation(required_fields=["name", "role"])
        .add_keywords_validation(["engineer", "Python"])
        .add_length_validation(min_length=20)
    )

    test_output = '{"name": "Charlie", "role": "Python engineer", "experience": 5}'
    passed, results = suite.run(test_output)

    print(f"Input: {test_output}")
    print(f"Overall: {'PASS' if passed else 'FAIL'}")
    for result in results:
        status = "✓" if result["passed"] else "✗"
        print(f"  {status} {result['name']}: {result['message']}")
