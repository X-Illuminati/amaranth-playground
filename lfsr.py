from amaranth import *
from amaranth.lib import *
from amaranth.lib.wiring import *

class LFSRDynamic(wiring.Component):
    def __init__(self, width=8, init=1):
        
        super().__init__({
            "taps": In(width),
            "out": Out(width, reset=init),
        })
        self.width=width
        self.initial=init

    def elaborate(self, platform):
        m = Module()

        oldtaps = Signal(self.width)
        nextbits = Signal(self.width)

        #check if the taps have changed and reset the LFSR register
        with m.If(self.taps != oldtaps):
            m.d.sync += self.out.eq(self.initial)
        with m.Else():
#            m.d.sync += nextbits.eq(1)
            m.d.sync += self.out.eq(Cat(nextbits.xor(), self.out))
        for i in range(self.width):
            with m.If(self.taps[i]):
                m.d.comb += nextbits[i].eq(self.out[i])
            with m.Else():
                m.d.comb += nextbits[i].eq(0)
        m.d.sync += oldtaps.eq(self.taps)

        return m

