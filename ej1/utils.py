def sumar_complemento_a_dos(n1,n2,bits_inputs,bits_sum):
	# recibe dos números binarios, 'n1' y 'n2' de 'bits_inputs' bits. Realiza la suma
	# complemento a 2 y la devuelve expresada en 'bits_sum'. Si se le pasa 
	# 'bits_sum' < 'bits_inputs', la función asume que 'bits_inputs' = 'bits_sum'.

    # esta máscara se usa para chekear el bit más significativo del número
    # y ver si es negativo o positivo
    mask_check_msb = int('1',2)<<(bits_inputs-1)
    
    # esta máscara sirve para agregar los 1's que correspondan a la izquierda del número,
    # en caso de que este sea negativo.
    mask_extend_width = int('1'*(bits_sum-bits_inputs),2)<<bits_inputs

    # esta máscara sirve para eliminar el último bit, en caso de que luego de la suma
    # se tenga carry
    mask_sum = int('1'*bits_sum,2)

    if(bits_sum > bits_inputs):

        if((n1 & mask_check_msb) != 0):
            aux_1 = n1 | mask_extend_width
        else:
            aux_1 = n1
        if((n2 & mask_check_msb) != 0):
            aux_2 = n2 | mask_extend_width
        else:
            aux_2 = n2
    else:
        aux_1 = n1
        aux_2 = n2

    return (aux_1 + aux_2) & mask_sum