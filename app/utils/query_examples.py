import yaml
import os
from typing import List, Dict, Any, Optional


def load_query_examples(file_path: str = "query_examples.yml") -> List[str]:
    """
    Load query examples from a YAML file and format them for the Text2Cypher retriever.
    
    Args:
        file_path (str): Path to the YAML file containing query examples
        
    Returns:
        List[str]: List of formatted examples as strings
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"⚠️ Query examples file not found: {file_path}")
            return []
        
        # Load YAML file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        # Extract examples
        examples = data.get('query_examples', [])
        
        # Format examples for Text2Cypher
        formatted_examples = []
        for example in examples:
            input_text = example.get('input', '')
            output_cypher = example.get('output', '').strip()
            
            if input_text and output_cypher:
                formatted_example = f"User: {input_text}\nCypher: {output_cypher}"
                formatted_examples.append(formatted_example)
        
        print(f"✅ Loaded {len(formatted_examples)} query examples from {file_path}")
        return formatted_examples
        
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file {file_path}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading query examples from {file_path}: {e}")
        return []


def get_example_by_input(input_text: str, file_path: str = "query_examples.yml") -> Optional[str]:
    """
    Get a specific example by matching the input text.
    
    Args:
        input_text (str): The input text to search for
        file_path (str): Path to the YAML file
        
    Returns:
        Optional[str]: The matching Cypher query or None if not found
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        examples = data.get('query_examples', [])
        
        for example in examples:
            if example.get('input', '').lower() == input_text.lower():
                return example.get('output', '').strip()
        
        return None
        
    except Exception as e:
        print(f"❌ Error searching examples: {e}")
        return None


def add_query_example(input_text: str, output_cypher: str, file_path: str = "query_examples.yml") -> bool:
    """
    Add a new query example to the YAML file.
    
    Args:
        input_text (str): The natural language input
        output_cypher (str): The corresponding Cypher query
        file_path (str): Path to the YAML file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load existing data
        data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file) or {}
        
        # Initialize query_examples if not present
        if 'query_examples' not in data:
            data['query_examples'] = []
        
        # Add new example
        new_example = {
            'input': input_text,
            'output': output_cypher
        }
        
        # Check if example already exists
        for existing in data['query_examples']:
            if existing.get('input') == input_text:
                print(f"⚠️ Example already exists for: {input_text}")
                return False
        
        data['query_examples'].append(new_example)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Added new query example: {input_text}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding query example: {e}")
        return False 