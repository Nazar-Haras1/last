import json
import time
import random
from functools import wraps
import sys
import string



def logging_before(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"CALLING {func.__name__}: ARGS={args}, KWARGS={kwargs}")
        return func(*args, **kwargs)
    return wrapper


def logging_after(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"PROCESSED {func.__name__}: RESULT={result}")
        return result
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"TIMER LOG: {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def access_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with open("main.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError("json not found!")

            username = input("Enter your name: ")

            user = next((u for u in users if u["name"] == username), None)

            if not user:
                raise PermissionError(f"User '{username}' not found!")

            if user["access_right"] != required_role:
                raise PermissionError(
                    f"Access denied for {username}. "
                    f"Required role: {required_role}, but got {user['access_right']}"
                )

            print(f"Access granted for {username} with role {required_role}")
            return func(*args, **kwargs)
        return wrapper
    return decorator



def sort_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            sorted_result = sorted(result)
            print(f"SORTED RESULT: {sorted_result}")
            return sorted_result
        return result
    return wrapper



@logging_before
@logging_after
@timer
@sort_result
@access_required("admin")
def get_shuffled_alphabet():
    import random
    import string
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    print("Shuffled alphabet:", letters)  
    return letters
if __name__ == "__main__":
    try:
        result = get_shuffled_alphabet()
        print(f"\nFinal result returned from get_shuffled_alphabet: {result}")
    except PermissionError as e:
        print(f" Access error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")