#!/usr/bin/env python3
"""
Knowledge Index Validator
知識索引驗證工具

Validates the docs/knowledge_index.yaml file to ensure:
- All referenced files exist
- Required fields are present
- IDs are unique
- Relationships reference valid documents

Usage:
    python tools/docs/validate_index.py
    python tools/docs/validate_index.py --verbose
"""

import argparse
import sys
from pathlib import Path
from typing import Any

# Try to import yaml, provide helpful error if not available
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_index(index_path: Path) -> dict[str, Any]:
    """Load and parse the knowledge index YAML file."""
    with open(index_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_required_fields(doc: dict[str, Any], doc_id: str) -> list[str]:
    """Check that all required fields are present in a document entry."""
    required_fields = ['id', 'path', 'title', 'domain', 'layer', 'kind', 'status']
    errors = []
    for field in required_fields:
        if field not in doc:
            errors.append(f"Document '{doc_id}' missing required field: {field}")
    return errors


def validate_file_exists(doc: dict[str, Any], repo_root: Path) -> list[str]:
    """Check that the referenced file exists."""
    errors = []
    file_path = repo_root / doc['path']
    if not file_path.exists():
        errors.append(f"Document '{doc['id']}' references non-existent file: {doc['path']}")
    return errors


def validate_unique_ids(documents: list[dict[str, Any]]) -> list[str]:
    """Check that all document IDs are unique."""
    errors = []
    seen_ids = set()
    for doc in documents:
        doc_id = doc.get('id', '<unknown>')
        if doc_id in seen_ids:
            errors.append(f"Duplicate document ID: {doc_id}")
        seen_ids.add(doc_id)
    return errors


def validate_relationships(relationships: list[dict[str, Any]], doc_ids: set[str]) -> list[str]:
    """Check that all relationships reference valid document IDs."""
    errors = []
    for rel in relationships:
        if rel.get('from') not in doc_ids:
            errors.append(f"Relationship references unknown document: {rel.get('from')}")
        if rel.get('to') not in doc_ids:
            errors.append(f"Relationship references unknown document: {rel.get('to')}")
    return errors


def validate_domains(documents: list[dict[str, Any]], categories: dict[str, Any]) -> list[str]:
    """Check that all documents use valid domain categories."""
    errors = []
    valid_domains = set(categories.keys())
    for doc in documents:
        domain = doc.get('domain')
        if domain and domain not in valid_domains:
            errors.append(f"Document '{doc.get('id')}' uses unknown domain: {domain}")
    return errors


def validate_layers(documents: list[dict[str, Any]], layers: list[str]) -> list[str]:
    """Check that all documents use valid layers."""
    errors = []
    valid_layers = set(layers)
    for doc in documents:
        layer = doc.get('layer')
        if layer and layer not in valid_layers:
            errors.append(f"Document '{doc.get('id')}' uses unknown layer: {layer}")
    return errors


def main():
    parser = argparse.ArgumentParser(description='Validate knowledge index YAML file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    index_path = repo_root / 'docs' / 'knowledge_index.yaml'

    if not index_path.exists():
        print(f"Error: Knowledge index not found at {index_path}")
        sys.exit(1)

    if args.verbose:
        print(f"Validating: {index_path}")
        print(f"Repo root: {repo_root}")
        print()

    # Load the index
    try:
        index = load_index(index_path)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML syntax in {index_path}")
        print(str(e))
        sys.exit(1)

    documents = index.get('documents', [])
    categories = index.get('categories', {})
    layers = index.get('layers', [])
    relationships = index.get('relationships', [])

    if args.verbose:
        print(f"Found {len(documents)} documents")
        print(f"Found {len(categories)} categories")
        print(f"Found {len(layers)} layers")
        print(f"Found {len(relationships)} relationships")
        print()

    # Collect all errors
    all_errors = []

    # Validate unique IDs
    all_errors.extend(validate_unique_ids(documents))

    # Get all valid document IDs
    doc_ids = {doc.get('id') for doc in documents if doc.get('id')}

    # Validate each document
    for doc in documents:
        doc_id = doc.get('id', '<unknown>')
        
        # Check required fields
        all_errors.extend(validate_required_fields(doc, doc_id))
        
        # Check file exists
        if 'path' in doc:
            file_errors = validate_file_exists(doc, repo_root)
            all_errors.extend(file_errors)

    # Validate domains
    all_errors.extend(validate_domains(documents, categories))

    # Validate layers
    all_errors.extend(validate_layers(documents, layers))

    # Validate relationships
    all_errors.extend(validate_relationships(relationships, doc_ids))

    # Output results
    if all_errors:
        print("❌ Validation FAILED")
        print()
        print(f"Found {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("✅ Validation PASSED")
        print()
        print(f"Summary:")
        print(f"  • {len(documents)} documents validated")
        print(f"  • {len(relationships)} relationships validated")
        print(f"  • All referenced files exist")
        print(f"  • All IDs are unique")
        sys.exit(0)


if __name__ == '__main__':
    main()
