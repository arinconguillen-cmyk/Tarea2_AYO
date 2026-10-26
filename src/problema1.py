import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt

def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == '__main__':
    seeds = list(range(8))
    
    # 1. Ejecución normal 
    t0 = time.perf_counter()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(estimate_pi, seeds)
    print(f"Normal (Todos los núcleos) - Tiempo: {time.perf_counter() - t0:.3f} s")
    
    # 2. Ejecución modificada: 1, 2, 4 y 8 procesos
    procesos = [1, 2, 4, 8]
    tiempos = {}
    speedups = []

    print("\nEjecución Modificada:")
    for p in procesos:
        t0 = time.perf_counter()
        with mp.Pool(processes=p) as pool:
            pool.map(estimate_pi, seeds)
        t_par = time.perf_counter() - t0
        tiempos[p] = t_par
        
        speedup = tiempos[1] / t_par if p > 1 else 1.0
        speedups.append(speedup)
        print(f"Procesos: {p} | Tiempo: {t_par:.3f} s | Speedup: {speedup:.2f}x")

    # 3. Generar gráfica
    plt.plot(procesos, speedups, marker='o', linestyle='-', color='b', label='Speedup Real')
    plt.plot(procesos, procesos, marker='', linestyle='--', color='r', label='Speedup Ideal (Lineal)')
    plt.title('Speedup Paralelo (Procesos vs Aceleración)')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.show()
