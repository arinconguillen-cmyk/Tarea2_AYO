import math
import random
import matplotlib.pyplot as plt

def tour_length(route, cities):
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
               for i in range(len(route)))

def two_opt_move(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

def full_2opt_count(route, cities):
    improvements = 0
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = two_opt_move(route, i, k)
                if tour_length(new_route, cities) < tour_length(route, cities):
                    route = new_route
                    improvements += 1
                    improved = True
                    break 
            if improved:
                break
    return route, improvements

def nearest_neighbour(cities, start_node):
    unvisited = list(cities.keys())
    tour = [start_node]
    unvisited.remove(start_node)
    current = start_node
    
    while unvisited:
        next_node = min(unvisited, key=lambda city: math.dist(cities[current], cities[city]))
        tour.append(next_node)
        unvisited.remove(next_node)
        current = next_node
        
    return tour

#Prueba
if __name__ == '__main__':
    random.seed(42) 
    cities = {f'C{i}': (random.uniform(0, 100), random.uniform(0, 100)) for i in range(15)}

    ruta_aleatoria = list(cities.keys())
    random.shuffle(ruta_aleatoria)
    dist_aleatoria_inicial = tour_length(ruta_aleatoria, cities)

    ruta_nn = nearest_neighbour(cities, 'C0')
    dist_nn_inicial = tour_length(ruta_nn, cities)

    ruta_aleatoria_final, mejoras_aleatoria = full_2opt_count(ruta_aleatoria, cities)
    ruta_nn_final, mejoras_nn = full_2opt_count(ruta_nn, cities)

    print("RESULTADOS")
    print(f"Distancia inicial ruta aleatoria: {dist_aleatoria_inicial:.2f}")
    print(f"Distancia inicial Nearest Neighbour: {dist_nn_inicial:.2f}\n")
    
    print(f"Mejoras necesarias desde ruta ALEATORIA: {mejoras_aleatoria}")
    print(f"Mejoras necesarias desde NEAREST NEIGHBOUR: {mejoras_nn}")

#Grafica
metodos = ['Ruta Aleatoria', 'Nearest Neighbour']
mejoras = [22, 2]
distancias = [330.86, 330.86] 

fig, ax1 = plt.subplots(figsize=(8, 4))

color = 'tab:blue'
ax1.set_xlabel('Método de Inicio')
ax1.set_ylabel('Número de Mejoras 2-opt', color=color)
bars = ax1.bar(metodos, mejoras, color=color, alpha=0.7, width=0.4)
ax1.tick_params(axis='y', labelcolor=color)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontweight='bold')

plt.title('Ejercicio 3: Número de Mejoras 2-opt según Solución Inicial')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
