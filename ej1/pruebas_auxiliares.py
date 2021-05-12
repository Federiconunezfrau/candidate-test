from random import getrandbits


def sumar_complemento_a_dos(n1,n2,bits_inputs,bits_sum):
	# recibe dos números binarios, 'n1' y 'n2' de 'bits_inputs' bits. Realiza la suma
	# complemento a 2 y la devuelve expresada en 'bits_sum'.

    mask_check_msb = int('1',2)<<(bits_sum-1)

    mask_sum = int('1'*bits_sum,2)

    if((n1 & mask_check_msb) != 0):
	    aux_1 = n1 | (mask_check_msb << (bits_sum - bits_inputs))

    if((n2 & mask_check_msb) != 0):
	    aux_2 = n2 | (mask_check_msb << (bits_sum - bits_inputs))

    return (aux_1 + aux_2) & mask_sum

N = 5	# cantidad de palabras de los datos
width = 5
width_out = width+1

data_a = [getrandbits(width) for _ in range(N)]
data_b = [getrandbits(width) for _ in range(N)]

mask = int('1' * (width_out), 2)

# genero la suma complemento a 2

print(data_a)
print(data_b)

mask_check_MSB = int('1',2)<<(width-1)

data_r = [(data_a[i] + data_b[i]) & mask for i in range(N)]
data_r_2 = [(data_a[i] + data_b[i]) for i in range(N)]
data_r_3 = []
for d in range(N):
    dato_de_a = data_a[d]	# tomo el dato correspondiente a 'a'
    dato_de_b = data_b[d]	# tomo el dato correspondiente a 'b'

    # se chequea el bit más significativo. Si es distinto de 0,
    # quiere decir que en complemento a 2, es negativo ==> se 
    # agregan unos a la izquierda del número hasta completar 
    # con la cantidad de bits requeridos.
    if((dato_de_b & mask_check_MSB) != 0):
    	dato_de_b = dato_de_b | (mask_check_MSB << (width_out - width))

    if((dato_de_a & mask_check_MSB) != 0):
    	dato_de_a = dato_de_a | (mask_check_MSB << (width_out - width))

    data_r_3.append((dato_de_a + dato_de_b) % mask)



    

#print(data_r)
#print(data_r_2)
print(data_r_3)