"""Sample Python file for testing the Docstring Generation Agent."""

class DataProcessor:
    """Process and transform data."""
    
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self._cache = {}
    
    def process_data(self, data, validate=True):
        if validate:
            self._validate_data(data)
        
        result = []
        for item in data:
            processed = self._transform_item(item)
            result.append(processed)
        
        return result
    
    def _validate_data(self, data):
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
    
    def _transform_item(self, item):
        return item.upper() if isinstance(item, str) else str(item)


def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


async def fetch_user_data(user_id: str, timeout: float = 30.0) -> dict:
    # Simulated async function
    await asyncio.sleep(0.1)
    return {"id": user_id, "name": "User"}


def create_report(title, data, format="pdf", include_summary=True):
    report = {
        "title": title,
        "data": data,
        "format": format,
    }
    
    if include_summary:
        report["summary"] = "Summary here"
    
    return report


class UserFactory:
    """Factory for creating user instances."""
    
    @staticmethod
    def create_user(username, email):
        return {"username": username, "email": email}


def is_valid_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
