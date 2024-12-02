from static import MD  # Импортируем ваш класс

# Пример матрицы и вероятностей
matrix = [
    [0.8, 0.1, 0.1],
    [0.2, 0.7, 0.1]
]

probabilities = {1: 0.6, 2: 0.4}
pbj = [0.5, 0.3, 0.2]

# Создаем объект MD
md = MD()

# Вычисляем энтропию
u_entropy = md.u_entropy(matrix, probabilities)
a_entropy = md.a_entropy(pbj)
final_entropy = md.final_entropy(matrix)

# Печатаем результаты
print("Условная энтропия H(B|A):")
print(u_entropy)

print("\nЭнтропия H(B):")
print(a_entropy)

print("\nОбщая энтропия H(A,B):")
print(final_entropy)
