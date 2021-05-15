import re
import sys
# ==================================================
def translate_mem_syntax_vendor(str_input,memdump_file_name):
    # recibe una string de entrada con el formato de verilog
    # y el nombre del archivo que contiene la info para la memoria.
    # Devuelve otra string con la sintaxis deseada.

    # se extrae la primera línea del string, la cual se pasa al archivo nuevo
    pattern = re.compile(r'  reg \[(.*)\] (\S*) \[(.*)\];\n')
    match = pattern.search(str_input)
    aux = "  $readmemh(\""+memdump_file_name+"\", mem);\n"
    str_output = match.group() + aux

    return str_output

# ==================================================
def generate_memdump_string(str_input):
    # recibe una string de entrada con el formato de verilog.
    # devuelve otra string que solamente contiene los elementos
    # de memoria.

    # se crea el pattern que se está buscando
    pattern = re.compile(r'(?<=[\d\s]\'[\w])[\w]*')
    match = pattern.findall(str_input)

    return match

# ==================================================
def main(input_file_name,output_file_name):
    
    # se intenta abrir el input file
    try:
        # si se pudo abrir, se prosigue con el script
        with open(input_file_name,'rt') as file_input:
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
            #file_output = open("expected_2.v",'wt')
            file_output = open(output_file_name,'wt')

            # este contador sirve para indicar el índice donde se encontró la coincidencia del
            # patrón deseado
            i = 0

            # este índice sirve para identificar cuántas coincidencias hubo. Se usa para darle
            # nombre a los archivos memdump, que se llamarán "memdump0.mem", "memdump1.mem", etc.
            j = 0
        
            while(match):

	            # se extrae la string del objeto 'match'
                string_to_translate = match.group()

                # se genera una lista con los datos de memoria para escribir en el archivo memdump
                list_memdump = generate_memdump_string(string_to_translate)

                # nombre del archivo correspondiente de memoria
                memdump_file_name = "memdump"+str(j)+".mem"
            
                # se crea el archivo nuevo de memdump y se escriben los datos correspondientes
                with open(memdump_file_name,'wt') as file_memdump:
                    for element in list_memdump:
                        file_memdump.write(element + "\n")

                # se traduce la string a la sintaxis deseada
                string_translated = translate_mem_syntax_vendor(string_to_translate,memdump_file_name)
        
                # se escribe sobre el archivo de salida, todo lo anterior a la ubicación de la primera
                # coincidencia, seguido de la string a la que se le modificó la sintaxis
                string_to_write = original[i:match.start()] + string_translated
                file_output.write(string_to_write)

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
        else:
            # si no hay coincidencia, no se hace nada
            print("no inline memory initialization found")
    
    # si no se pudo abrir el input file, luego se imprime un mensaje de error
    except IOError:
        print("File "+input_file_name+" not found.")

# ==================================================
if __name__== '__main__':
    
    # se chequea la cantidad de argumentos
    if(len(sys.argv)!=3):
        print("Incorrect number of arguments.")
    # si está ok, se prosigue con el script
    else:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
        main(input_file_name,output_file_name)