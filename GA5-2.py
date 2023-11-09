import numpy as np
from decimal import *
from rich.progress import Progress

# 2.23606797749979
pop_size = 100           # 總群數量
parent_size = 0.2       # 母體保留數量
binary_size = 192        # 位元長度
cross_rate = 1        # 基因交換率
mutation_rate = 0.015   # 變異率
N_generation = 75       # 迭代次數

best_fit = 1
best_binary = 0
getcontext().prec = 15

def trans_value(pop):
    bin_mask = [2**(-i) for i in range(1,(binary_size+1))] # 生成2^-1 ~ 2^-n的
    value_list = []
    for a in pop:
        value0 = np.multiply(a,bin_mask)
        value_list.append(sum(value0))
    return value_list

def trans_single_value(pop):
    bin_mask = [2**(-i) for i in range(1,(binary_size+1))] # 生成2^-1 ~ 2^-n的
    value0 = np.multiply(pop,bin_mask)
    return np.sum(value0)

def get_fitness(pop):
    pop_value = trans_value(pop)
    # print(pop)
    for i  in range(pop_size):
        pop_value[i] = abs(5-((2+pop_value[i])**2))
    # print(pop_value)
    return pop_value

def get_single_fitness(pop):
    pop_value = trans_single_value(pop)
    return abs(5-((2+pop_value)**2))

def crossover(pop,fitness):
    global parent_size
    child_pop_size = 0
    child_list = []
    # 總群相互配對
    for i in range(pop_size):
        for j in range(pop_size):
            if np.random.rand() < cross_rate:
                # Select
                cross_points = np.random.randint(0, 2, size=binary_size).astype(bool)     # choose crossover points
                parent_fitness = min(fitness[i],fitness[j])
                parent = [pop[i],pop[j]]
                child = [parent[1][tt] if cross_points[tt] else parent[0][tt] for tt in range(binary_size)]
                # Mutate
                for k in range(binary_size):
                    if np.random.rand() < mutation_rate and best_fit > 1e-4:
                        child[k] = 1 if child[k] == 0 else 0
                    elif np.random.rand() < 0.1:
                        child[k] = 1 if child[k] == 0 else 0
                if get_single_fitness(child) < parent_fitness and child_pop_size < int(pop_size*(1-parent_size)):
                    child_list.append(child)
                    child_pop_size+=1
                elif child_pop_size >= int(pop_size*(1-parent_size)):
                    break
        if child_pop_size >= int(pop_size*(1-parent_size)):
            break
    # 子代未有改善 使用母體最高
    fitness_pos = np.argsort(fitness)
    for i in fitness_pos:
        if len(child_list) >= pop_size:
            break
        child_list.append(pop[i])
    return child_list
    # print(pop)
    # print(child_lsit)
    # print("cross parent1: ",parent[0])
    # print("cross parent2: ",parent[1])
    # print(cross_points)
    # print("child: ",child)
        # parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
    # if np.amax(get_fitness_single(parent)) > best_fitness:
    # return parent
    # else:
        # return parent_copy
# main
pop = np.random.randint(0,2,(pop_size,binary_size))
# print(pop)
with Progress() as progress:
    task1 = progress.add_task("[green bold]Crossover...",total=N_generation)
    while not progress.finished :
        pop_value = trans_value(pop)
        pop_fitness = get_fitness(pop_value)
        child_pop = crossover(pop,pop_fitness)
        # print(child_pop)
        child_fitness = get_fitness(child_pop)
        fitness_pos = np.argmin(child_fitness)
        if child_fitness[fitness_pos] < best_fit:
            best_fit = child_fitness[fitness_pos]
            best_binary = child_pop[fitness_pos]
            print(best_fit)
        if best_fit < 1e-13:
            print("fitness < 1e-13")
            break
        pop = child_pop
        progress.advance(task1,1)
best_value = trans_single_value(best_binary)
print("best sqrt:",(2+Decimal(f'{best_value}'))**2)
print("best:",(2+Decimal(f'{best_value}')))