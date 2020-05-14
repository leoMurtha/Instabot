from itertools import permutations, combinations   
import random

friends = ['@lucaporto', '@leououu', '@antonioomoreira', '@vitubrisola']

combs = list(combinations(friends, 2))

random.shuffle(combs)

print(combs)
