from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import getrandbits

# en este archivo agrego funciones de utilidades
from utils import sumar_complemento_a_dos

# =======================================================
'''
Clase Stream
'''

class Stream(Record):

    def __init__(self, width, **kwargs):
        Record.__init__(self, [('data', width), ('valid', 1), ('ready', 1)], **kwargs)
        # record is a bundle of signals. 
        # por eso cuando paso name = 'a', se crean las señales a__data, a__valid y a__ready


    def accepted(self):
        return self.valid & self.ready

    class Driver:
        def __init__(self, clk, dut, prefix):
            self.clk = clk
            self.data = getattr(dut, prefix + 'data')
            self.valid = getattr(dut, prefix + 'valid')
            self.ready = getattr(dut, prefix + 'ready')

        async def send(self, data):
            self.valid <= 1
            for d in data:
                self.data <= d
                await RisingEdge(self.clk)
                while self.ready.value == 0:
                    await RisingEdge(self.clk)
            self.valid <= 0

        async def recv(self, count):
            self.ready <= 1
            data = []
            for _ in range(count):
                await RisingEdge(self.clk)
                while self.valid.value == 0:
                    await RisingEdge(self.clk)
                data.append(self.data.value.integer)
            self.ready <= 0
            return data
# =======================================================
'''
Clase Adder
'''
class Adder(Elaboratable):

    # constructor, recibe una variable 'width_in' y otra 'width_out'.
    # La primera es la cantidad de bits de las streams de entrada 'a' y 'b' y la segunda es la cantidad de bits
    # para el stream de salida 'r'.
    def __init__(self, width_in,width_out):
        self.a = Stream(width_in, name='a')    # stream de datos, de 'width_in' bits, que se la identifica con el nombre 'a'
        self.b = Stream(width_in, name='b')    # stream de datos, de 'width_in' bits, que se la identifica con el nombre 'b'
        self.r = Stream(width_out, name='r')   # ídem pero que se identifica con el nombre 'r'. Tiene 'width_out' bits

    def elaborate(self, platform):
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        # mask_check_msb = int('1',2)<<(len(self.a__)-1) # esta maścara sirve para conocer el bit maś significativo de los datos de entrada.

        # Se chequea si 'r' fue aceptada
        with m.If(self.r.accepted()):
            # si fue aceptada, luego se agrega la regla de que, en el próximo rise del clock, r.valid sea igual a 0, es decir False.
            sync += self.r.valid.eq(0)

        # Se chequea si ambas señales de entrada fueron aceptadas
        with m.If(self.a.accepted() & self.b.accepted()):
            # si lo fueron, luego se agregan las reglas de que, en el próximo rise del clock, r.valid sea igual a 1, es decir True.
            # y de que r.data sea igual a la suma de los datos de 'a' y 'b''
            sync += [
                self.r.valid.eq(1),
                self.r.data.eq(self.a.data.as_signed() + self.b.data.as_signed())
            ]

        # esta regla hace que a.ready sea siempre igual a ((NOT r.valid) OR (r.accepted()))
        comb += self.a.ready.eq((~self.r.valid) | (self.r.accepted()))
        comb += self.b.ready.eq((~self.r.valid) | (self.r.accepted()))
        return m
# =======================================================
'''
Funciones pertinentes al testeo
'''
# en init_test se crea un proceso que corre un clock de 10 ns y lo pone a correr. Se esperan 2 rises del clock y después termina.
async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 2, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    #await RisingEdge(dut.clk)
    dut.rst <= 0


# Esta es la prueba que se corre
@cocotb.test()
async def burst(dut):

    # llama a la función init_test y se queda esperando a que termine
    await init_test(dut)

    # 
    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    N = 5	# cantidad de palabras de los datos
    width_in = len(dut.a__data)
    width_out = len(dut.r__data)
    
    # se genera una lista de números enteros, aleatorios, usando 'width' bits (para el ejemplo 5), y de largo N, o sea 100.
    data_a = [getrandbits(width_in) for _ in range(N)]
    data_b = [getrandbits(width_in) for _ in range(N)]

    # se genera el expected de datos
    # expected = [(data_a[d] + data_b[d]) & mask for d in range(N)]
    expected = [sumar_complemento_a_dos(data_a[i],data_b[i],width_in,width_out) for i in range(N)]

    # se forkea otro proceso 'send'. El proceso toma los datos de 'data' y los coloca uno por uno en lo que llama 'stream_input'.
    # Luego de colocar el dato, se suspende el proceso 'send' hasta que ocurre un rise en el clock. De esta forma se simula el
    # envío de datos.
    cocotb.fork(stream_input_a.send(data_a))
    cocotb.fork(stream_input_b.send(data_b))

    # luego de forkear, se llama al proceso recv para el stream_output y se espera a que este termine. recv lo que hace es que
    # en cada rise del clock, si r.valid es 1  ==> se copia el valor de r.data en en la lista 'data', definida dentro de recv.
    # Finalmente 'recv' devuelve esta lista.
    recved = await stream_output.recv(N)

    # se chequea si recved, es decir, los datos recibidos, coinciden con los datos esperados
    assert recved == expected

# =======================================================
'''
Main programa
'''
# Inicico del programa

if __name__ == '__main__':

    N_in = 5          # cantidad de bits de las streams de entrada 'a' y 'b'
    N_out = N_in+5    # cantidad de bits del stream de salida, 'r''

    core = Adder(N_in,N_out) # "core" es una instancia de la clase Adder
    run(
        core, 'entrega_ej_1',
        ports=
        [
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='adder.vcd'
    )