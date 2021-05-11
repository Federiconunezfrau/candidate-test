from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import getrandbits
'''
NOTA: <= en cocotb es para asignar un valor a una señal. Por ejemplo dentro de la clase Driver hay una línea que dice
self.valid <= 1. Esto equivale (según la documentación) a self.valid.value = 1.
'''

'''
Clase 'Stream'.
Atributos:
    

Métodos:
    accepted(): devuelve True o False. Indica si el dato es leído puede ser leído por el sumidero o no

'''
class Stream(Record):

    def __init__(self, width, **kwargs):
        Record.__init__(self, [('data', width), ('valid', 1), ('ready', 1)], **kwargs)


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

'''
Clase Incrementador: es una clase heredada de Elaboratable.

Atributos:
    a: es un stream 
    r: es un stream
métodos:
    elaborate:

'''

class Incrementador(Elaboratable):

    # constructor, recibe una variable 'width'. Esta se usa para los atributos 'a' y 'r'
    def __init__(self, width):
        self.a = Stream(width, name='a')    # stream de datos, de 'width' bits, que se la identifica con el nombre 'a'
        self.r = Stream(width, name='r')    # ídem pero que se identifica con el nombre 'r'

    def elaborate(self, platform):
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        # Se chequea si 'r' fue aceptada
        with m.If(self.r.accepted()):
            # si fue aceptada, luego se agrega la regla de que, en el próximo rise del clock, r.valid sea igual a 0, es decir False.
            sync += self.r.valid.eq(0)

        # Se chequea si 'a' fue aceptada
        with m.If(self.a.accepted()):
            # si fue aceptada, luego se agregan las reglas de que, en el próximo rise del clock, r.valid sea igual a 1, es decir True.
            # y de que r.data sea igual a 'a.data + 1'
            sync += [
                self.r.valid.eq(1),
                self.r.data.eq(self.a.data + 1)
            ]
        # esta regla hace que a.ready sea siempre igual a ((NOT r.valid) OR (r.accepted()))
        comb += self.a.ready.eq((~self.r.valid) | (self.r.accepted()))
        return m

# en init_test se crea un proceso que corre un clock de 10 ns y lo pone a correr. Se esperan 2 rises del clock y después termina.
async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


# Esta es la prueba que se corre
@cocotb.test()
async def burst(dut):

    # llamaa a la función init_test y se queda esperando a que termine
    await init_test(dut)

    # 
    stream_input = Stream.Driver(dut.clk, dut, 'a__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    N = 100
    width = len(dut.a__data)
    mask = int('1' * width, 2)

    # se genera una lista de números enteros, aleatorios, usando 'width' bits (para el ejemplo 5), y de largo N, o sea 100.
    data = [getrandbits(width) for _ in range(N)]
    expected = [(d + 1) & mask for d in data]

    # se forkea otro proceso 'send'. El proceso toma los datos de 'data' y los coloca uno por uno en lo que llama 'stream_input'.
    # Luego de colocar el dato, se suspende el proceso 'send' hasta que ocurre un rise en el clock. De esta forma se simula el
    # envío de datos.
    cocotb.fork(stream_input.send(data))

    # luego de forkear, se llama al proceso recv para el stream_output y se espera a que este termine. recv lo que hace es que
    # en cada rise del clock, si r.valid es 1  ==> se copia el valor de r.data en en la lista 'data', definida dentro de recv.
    # Finalmente 'recv' devuelve esta lista.
    recved = await stream_output.recv(N)

    # se chequea si recved, es decir, los datos recibidos, coinciden con los datos esperados
    assert recved == expected


# Inicico del programa

if __name__ == '__main__':

    core = Incrementador(5) # "core" es una instancia de la clase Incrementador.EL NÚMERO INDICA LA CANTIDAD DE BITS DEL STREAM!
    run(
        core, 'example',
        ports=
        [
            *list(core.a.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='incrementador.vcd'
    )