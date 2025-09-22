from typing import TypedDict, Callable
import pickle
import os


def cached(key: str, callback: Callable):
    def wrapper(state: object) -> object:
        if not os.path.exists("cache"):
            os.makedirs("cache")

        if os.path.exists(f"cache/{key}.pkl"):
            with open(f"cache/{key}.pkl", "rb") as f:
                return pickle.load(f)
        else:
            result = callback(state)
            with open(f"cache/{key}.pkl", "wb") as f:
                pickle.dump(result, f)
            return result

    return wrapper
