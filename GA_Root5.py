import random

#根號5=2.2360679775
gene_length = 37 #22360679775轉為二進制的長度
population_size=100 #每一代染色體的數量
mutation_rate = 0.4 #變異機率

def Binary(num):
    #轉成2進制(str)
    binary_string=bin(num)[2:]
    return binary_string

def decimal_number(num):
    #轉乘10進制(str)
    return int(num,2)

def generate_population(population_size,gene_length):
    #隨機產生第一代父母(染色體)
    #poopularion_size為一代父母的數量(染色體)
    #gene_length 為染色體中基因的數量
    return[''.join(random.choice('01') for _ in range(gene_length)) for _ in range(population_size)]

def fitness(individual):
    #自適應函數
    #算出平方後與
    #分數越大代表越好
    num=decimal_number(individual)/(10**10)
    score=100000-abs(num**2-5)
    return score

def select_parents(population):
    #選擇2個染色體(當父母)
    #population為這一代中所有的父母
    return random.choices(population, k=2, weights=[fitness(ind) for ind in population])

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
    #隨機產生第一代染色體
    population=generate_population(population_size,gene_length)
    generation=0 #代數

    while True:
        generation+=1
        #對染色替做排序評分高的排前面
        population=sorted(population,key=fitness,reverse=True)
        new_population=[population[0]]
        #產生下一代(population_size個染色體)
        while len(new_population)<population_size:
            #選父母生小孩
            parent1,parent2=select_parents(population)
            child1,child2=crossover(parent1,parent2)

            #變異
            if random.random()<mutation_rate:
                child1=mutate(child1)
            if random.random()<mutation_rate:
                child2=mutate(child2)

            new_population.extend([child1,child2])

        population=new_population
        
        #這一代的最佳解
        ans=population[0]
        threshold=fitness(ans)
        print(f"Generation {generation}: {ans}, Fitness: {threshold}")

        if -0.0000000001<100000-threshold and 100000-threshold<0.0000000001:
            break
    
    print('根號5小數點後10位:',decimal_number(ans)/10**10)
    print('平方後:',(decimal_number(ans)/10**10)**2)

if __name__== '__main__':
    genetic_algorithm()