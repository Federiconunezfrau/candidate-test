from random import getrandbits

N = 5	# cantidad de palabras de los datos
width = 5

data_a = [getrandbits(width) for _ in range(N)]
data_b = [getrandbits(width) for _ in range(N)]

mask = int('1' * (width), 2)

# genero la suma complemento a 2

print(data_a)
print(data_b)

data_r = [(data_a[i] + data_b[i]) & mask for i in range(N)]
data_r_2 = [(data_a[i] + data_b[i]) for i in range(N)]

print(data_r)
print(data_r_2)