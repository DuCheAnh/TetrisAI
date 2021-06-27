import numpy
import genetic_alg as ga

f = open("record.txt", "w")

num_weights = 4
sol_per_pop = 10 # individual per popultion
num_generations = 5 #number of generation
num_parents_mating = 4 #how much mating pairs
pieceLimit=100 # number of piece till individual ends
seed=-1 # seeds: if seed<0: random else random.seed = seed

pop_size = (sol_per_pop,num_weights)
new_population = numpy.random.uniform(low=-2.0, high=2.0, size=pop_size)
print(new_population)

for generation in range(num_generations):
    print("Generation : ", generation)
    f.write(f"Generation: {generation}\n")
    fitness = ga.cal_pop_fitness(new_population,pieceLimit,seed)
    print(fitness)
    f.write(f"{fitness}\n")
    parents = ga.select_mating_pool(new_population, fitness,num_parents_mating)
    offspring_crossover = ga.crossover(parents,offspring_size=(pop_size[0]-parents.shape[0], num_weights))
    offspring_mutation = ga.mutation(offspring_crossover)
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

fitness = ga.cal_pop_fitness(new_population,pieceLimit,seed)
best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][0]

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])
f.write(f"Best solution: {new_population[best_match_idx,:]}\n")
f.write(f"best solution fitness: {fitness[best_match_idx]}\n")
f.close()