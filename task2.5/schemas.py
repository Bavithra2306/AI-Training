

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_user",
            "description": "Fetch a user by their user ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user to fetch."
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation using two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number."
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number."
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "The mathematical operation to perform."
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    }
]