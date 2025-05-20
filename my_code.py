# task 2 1 7

import sys

pokemons = [line.rstrip() for line in sys.stdin]
pokemons_set = set(pokemons)
print(len(pokemons) - len(pokemons_set))
