import re

# ==================================================
def translate_mem_syntax_vendor(str_input):
    # recibe una string de entrada con el formato de verilog.
    # devuelve otra string con la sintaxis deseada

    # TODO
    str_output = str_input
    return str_output

# ==================================================
def generate_memdump_string(str_input):
    # recibe una string de entrada con el formato de verilog.
    # devuelve otra string que solamente contiene los elementos
    # de memoria.

    # TODO
    str_output = str_input
    return str_output

# ==================================================
# se levanta el archivo original en modo lectura. Luego se cierra al salir de with
def main():

    with open('testcase_2.v','rt') as file_input:
        original = file_input.read()

    # se crea la regular expression
    pattern_memory_syntax = re.compile(r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')

    # se busca si hay coincidencias con el pattern_memory_syntax, en la string que contiene
    # el texto del archivo
    match = pattern_memory_syntax.search(original,0,len(original))

    # en caso de haber al menos una coincidencia, entonces se crea el archivo nuevo 
    # sobre el que se va a escribir. Luuego se siguen buscando coincidencias
    # y se las escribe.
    if(match):
    
        # se crea y se abre el archivo sobre el que se va a escribir con la sintaxis deseada
        file_output = open("expected_2.v",'wt')

        # este contador sirve para indicar el índice donde se encontró la coincidencia del
        # patrón deseado
        i = 0

        # este índice sirve para identificar cuántas coincidencias hubo. Se usa para darle
        # nombre a los archivos memdump, que se llamarán "memdump0.mem", "memdump1.mem", etc.
        j = 0

        while(match):

	        # se extrae la string del objeto 'match'
            string_to_translate = match.group()

            # se traduce la string a la sintaxis deseada
            string_translated = translate_mem_syntax_vendor(string_to_translate)
        
            # se escribe sobre el archivo de salida, todo lo anterior a la ubicación de la primera
            # coincidencia, seguido de la string a la que se le modificó la sintaxis
            string_to_write = original[i:match.start()] + string_translated
            file_output.write(string_to_write)

            # se genera la string con los datos de memoria para escribir en el archivo memdump
            string_memdump = generate_memdump_string(string_to_translate)
        
            # nombre del archivo correspondiente de memoria
            memdump_file_name = "memdump"+str(j)+".mem"

            # se crea el archivo nuevo de memdump y se escriben los datos correspondientes
            with open(memdump_file_name,'wt') as file_memdump:
                file_memdump.write(string_memdump)

            # se define el nuevo índice para seguir buscando en la string del
            # archivo original
            i = match.end()

            # se siguen buscando coincidencias
            match = pattern_memory_syntax.search(original,i,len(original))

            # se incrementa el contador de matches
            j+=1
    
        # se escribe lo que quedó proveniente del texto original
        file_output.write(original[i:])
    
        # se cierra el archivo de sintaxis nueva
        file_output.close()

    # si no hay coincidencia, no se hace nada

# ==================================================
if __name__=='main':
    main()