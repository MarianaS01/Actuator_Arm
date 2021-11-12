from evolution.evolution import Evolution

E = Evolution(0.8, 0.9, 1)

E.set_population(0, 10, 3, 3)
X = E.get_population()
#print(X)
E.update_FO(0, 1)
print(E.get_population())