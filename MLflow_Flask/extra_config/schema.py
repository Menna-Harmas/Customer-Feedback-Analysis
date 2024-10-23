# schema.py
import json

def get_input_schema():
    schema = {
        "input": {
            "type": "object",
            "properties": {
                "review_amount": {"type": "number"},
                "term": {"type": "number"},
                "interest_rate": {"type": "number"},
                "employment_length": {"type": "string"},
                "home_ownership": {"type": "string", "enum": ["RENT", "OWN", "MORTGAGE"]},
                "annual_income": {"type": "number"},
                "credit_score": {"type": "number"},
                "debt_to_income_ratio": {"type": "number"},
            },
            "required": ["review_amount", "term", "interest_rate", "employment_length", "home_ownership", "annual_income", "credit_score", "debt_to_income_ratio"],
        },
    }
    return json.dumps(schema)
