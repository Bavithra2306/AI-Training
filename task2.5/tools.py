


def fetch_user(user_id: int):
    users = {
        101: {
            "name": "Banu",
            "email": "banu@example.com"
        },
        102: {
            "name": "John",
            "email": "john@example.com"
        },
        103: {
            "name": "Priya",
            "email": "priya@example.com"
        }
    }

    user = users.get(user_id)

    if user is None:
        return {
            "error": "User not found"
        }

    return user


def calculate(a: float, b: float, operation: str):
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            return {
                "error": "Cannot divide by zero"
            }

        return a / b

    return {
        "error": "Unknown operation"
    }