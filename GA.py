import random


gene_length = 192 #binary length
population_size= 1000 #The number of chromosomes in each generation
mutation_rate = 0.4 #Mutation probability
tolerance = 1e-15   # Stop condition
aus = 1e2
# Enter the target number to be calculated
target = float(input("請輸入您要計算的根號值："))

def Binary(chromosome):
    #Convert to binary(str)
    binary_string=bin(chromosome)[2:]
    return binary_string

def decimal_number(chromosome):
    #轉乘10進制(str)
    return int(chromosome,2)

def generate_population(population_size,gene_length):
    return[''.join(random.choice('01') for _ in range(gene_length)) for _ in range(population_size)]


def fitness_function(individual):
    chromosome = decimal_number(individual) / (10**11)
    score = abs(aus - abs(chromosome**2 - target))
    return max(score, 0)  # 确保适应度值大于等于零

def select_parents(population):
    #選擇2個染色體(當父母)
    #population為這一代中所有的父母
    return random.choices(population, k=2, weights=[fitness_function(ind) for ind in population])

def crossover(parent1, parent2):
    #單點交叉(交配)
    #(1, len(parent1) - 2)是為了避免選到投跟尾
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual):
    #選擇一個點進行變異
    #使1-->0 和 0-->1
    mutated_index = random.randint(0, len(individual) - 1)
    mutated_gene = '0' if individual[mutated_index] == '1' else '1'
    return individual[:mutated_index] + mutated_gene + individual[mutated_index+1:]

def genetic_algorithm():
    #Randomly generate the first generation chromosomes
    population=generate_population(population_size,gene_length)
    generation=0 

    while True:
        generation+=1
        #Rank dyeing replacements with high scores ranked first
        population=sorted(population,key=fitness_function,reverse=True)
        new_population=[population[0]]
        #Generate the next generation (population_size chromosomes)
        while len(new_population)<population_size:
            #Choose parents to have children
            parent1,parent2=select_parents(population)
            child1,child2=crossover(parent1,parent2)

            #Mutations
            if random.random()<mutation_rate:
                child1=mutate(child1)
            if random.random()<mutation_rate:
                child2=mutate(child2)

            new_population.extend([child1,child2])

        population=new_population
        
        #The best solution of this generation
        ans=population[0]
        a=fitness_function(ans)
        print(f"Generation {generation}: {ans}")
        # Check whether the stopping condition is met
        if -tolerance < aus - a < tolerance:
            break
        # print(f"100 - a: {100 - a}")
        # print(f"a - target = {a - target}")

    print('祝所有的AIIA學長都可以準時畢業離校')
    print(f'Root {int(target)} :', decimal_number(ans) / 10**11)
    print(f'Closest target number {int(target)} :', (decimal_number(ans) / 10**11)**2)

if __name__ == '__main__':
    genetic_algorithm()
    
    
    
# ans = # 2.23606797749979