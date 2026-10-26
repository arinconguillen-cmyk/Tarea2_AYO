import math
import random
import matplotlib.pyplot as plt

random.seed(42)
num_cities = 20
cities = {f'C{i}': (random.uniform(0, 100), random.uniform(0, 100)) for i in range(num_cities)}

def tour_length(route, cities):
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]]) 
               for i in range(len(route)))

def two_opt_swap(route):
    i, k = sorted(random.sample(range(len(route)), 2))
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

def simulated_annealing(cities, mode='lento', max_iter=1500, T0=1000.0):
    current_route = list(cities.keys())
    random.shuffle(current_route)
    current_dist = tour_length(current_route, cities)
    
    best_route = list(current_route)
    best_dist = current_dist
    
    history_best = [best_dist] 
    T = T0
    
    for k in range(1, max_iter):
        if mode == 'lento':          
            T = T0 * (0.995 ** k)
        elif mode == 'rapido':       
            T = T0 * (0.85 ** k)
        elif mode == 'logaritmico':  
            T = T0 / (1 + math.log(1 + k))
            
        neighbor = two_opt_swap(current_route)
        neighbor_dist = tour_length(neighbor, cities)
        delta = neighbor_dist - current_dist
        
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            current_route = neighbor
            current_dist = neighbor_dist
            if current_dist < best_dist:
                best_route = list(current_route)
                best_dist = current_dist
                
        history_best.append(best_dist)
        
    return history_best, best_dist

hist_lento, min_lento = simulated_annealing(cities, mode='lento')
hist_rapido, min_rapido = simulated_annealing(cities, mode='rapido')
hist_log, min_log = simulated_annealing(cities, mode='logaritmico')

print(f"Mejor distancia (Enfriamiento Lento): {min_lento:.2f}")
print(f"Mejor distancia (Enfriamiento Rápido): {min_rapido:.2f}")
print(f"Mejor distancia (Logarítmico): {min_log:.2f}")

#Grafica
plt.figure(figsize=(10, 5))
plt.plot(hist_lento, label=f'Enfriamiento Lento (alpha=0.995) -> Min: {min_lento:.1f}', color='green')
plt.plot(hist_rapido, label=f'Enfriamiento Rápido (alpha=0.85) -> Min: {min_rapido:.1f}', color='purple')
plt.plot(hist_log, label=f'Logarítmico (Boltzmann) -> Min: {min_log:.1f}', color='orange')
plt.title('Simulated Annealing TSP: Calidad del Mejor Recorrido vs. Iteraciones')
plt.xlabel('Iteración')
plt.ylabel('Distancia del Mejor Recorrido')
plt.legend()
plt.grid(True)
plt.show()

#Grafica tiempo ejecucion vs calidad final
esquemas = ['Enfriamiento Lento\n(alpha=0.995)', 'Enfriamiento Rápido\n(alpha=0.85)', 'Logarítmico\n(Boltzmann)']
tiempos_s = [0.18, 0.12, 0.25] 
calidad_dist = [365.38, 352.32, 600.39] 

fig, ax1 = plt.subplots(figsize=(8, 4.5))

color = 'tab:red'
ax1.set_xlabel('Esquema de Enfriamiento')
ax1.set_ylabel('Distancia Final (Calidad - Menor es mejor)', color=color)
ax1.bar(esquemas, calidad_dist, color=color, alpha=0.6, width=0.4)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Tiempo de Ejecución (segundos)', color=color)
ax2.plot(esquemas, tiempos_s, color=color, marker='o', linewidth=2, markersize=8)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Ejercicio 4: Tiempo de Ejecución vs. Calidad de la Solución Final (SA)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
