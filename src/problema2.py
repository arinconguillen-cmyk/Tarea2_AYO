def greedy_ratio(items, capacity):
    # Ordena por mayor ratio
    sorted_items = sorted(items, key=lambda x: x['v'] / x['w'], reverse=True)
    total_value = 0
    for item in sorted_items:
        if item['w'] <= capacity:
            total_value += item['v']
            capacity -= item['w']
    return total_value

def greedy_lowest_weight(items, capacity):
    # Ordena priorizando el menor peso
    sorted_items = sorted(items, key=lambda x: x['w'])
    total_value = 0
    for item in sorted_items:
        if item['w'] <= capacity:
            total_value += item['v']
            capacity -= item['w']
    return total_value

# Prueba
items = [
    {'name': 'A', 'v': 10, 'w': 10},
    {'name': 'B', 'v': 20, 'w': 20},
    {'name': 'C', 'v': 1000, 'w': 40}
]
print(f"Mejor valor (Ratio v/w): {greedy_ratio(items, 50)}")
print(f"Mejor valor (Menor Peso): {greedy_lowest_weight(items, 50)}")
