import os
import openai
from dotenv import load_dotenv


def jp(L: list, k: int) -> list:
    i = 0
    result = []
    while len(L) != 0:
        # avance par pas de k (modulo len(l) pour pas sortir de l'index)
        i = (i + k - 1) % len(L)
        # prochain a se suicider
        result.append(L.pop(i))

    return result


if __name__ == "__main__":
    l = [1, 2, 3, 4, 5, 6, 7]
    print(jp(l, 3))
