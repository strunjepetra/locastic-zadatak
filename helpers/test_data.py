from datetime import datetime

def make_unique_email():
    timestamp=datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"john.doe.{timestamp}@example.com"