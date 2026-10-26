import math
import random
import itertools
import matplotlib.pyplot as plt

def mst_prim(points):
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, len(points))}
    children = {v: [] for v in range(len(points))}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children

def preorder(children, root=0):
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def tour_length(points, tour):
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def two_opt_move(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

def apply_2opt(route, points):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route)):
                if k - i == 1: continue
                new_route = two_opt_move(route, i, k)
                if tour_length(points, new_route) < tour_length(points, route):
                    route = new_route
                    improved = True
        if improved: break
    return route

if __name__ == '__main__':
    random.seed(123) 
    
    ratios_mst = []
    ratios_2opt = []
    instancias = list(range(1, 101)) 
    
    print("Calculando 100 instancias de 9 ciudades")
    
    for _ in instancias:
        points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(9)]
        
        optimal_tour = min(((0,) + p for p in itertools.permutations(range(1, 9))),
                           key=lambda t: tour_length(points, t))
        l_opt = tour_length(points, optimal_tour)
        
        mst_tour = preorder(mst_prim(points))
        l_mst = tour_length(points, mst_tour)
        ratios_mst.append(l_mst / l_opt)
        
        tour_mejorado = apply_2opt(mst_tour, points)
        l_2opt = tour_length(points, tour_mejorado)
        ratios_2opt.append(l_2opt / l_opt)

    promedio_mst = sum(ratios_mst) / 100
    promedio_2opt = sum(ratios_2opt) / 100

    print("RESULTADOS")
    print(f"Promedio Ratio MST Normal: {promedio_mst:.3f}")
    print(f"Promedio Ratio MST Modificado (+ 2-opt): {promedio_2opt:.3f}")
    print(f"Garantía teórica máxima del MST: 2.000")

    plt.scatter(instancias, ratios_mst, color='blue', alpha=0.6, label='MST Normal')
    plt.scatter(instancias, ratios_2opt, color='green', alpha=0.6, label='MST Modificado (+2-opt)')
    plt.axhline(y=2.0, color='red', linestyle='--', label='Garantía Máxima (Ratio = 2)')
    plt.axhline(y=1.0, color='black', linestyle='-', label='Óptimo Absoluto (Ratio = 1)')
    
    plt.title('Ratio de Aproximación: MST vs MST+2-opt (100 instancias)')
    plt.xlabel('Instancia #')
    plt.ylabel('Ratio (Costo / Óptimo)')
    plt.legend()
    plt.grid(True)
    plt.show()

#Grafica comparativa
metodos = ['Búsqueda Local\n(2-opt)', 'Recocido Simulado\n(SA Lento)', 'MST Puro', 'MST + 2-opt']
costos_promedio = [350.2, 365.38, 385.1, 352.1] 

plt.figure(figsize=(9, 4.5))
bars = plt.bar(metodos, costos_promedio, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.85)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')

plt.ylabel('Costo Promedio del Recorrido (Distancia)')
plt.title('Ejercicio 5: Comparativa de Costo Final entre Todos los Métodos')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
