from amaranth import *
from amaranth.lib import *
from amaranth.lib.wiring import *

class SevenSegmentDisp(wiring.Component):
    bcd: In(4)
    seg_a: Out(1)
    seg_b: Out(1)
    seg_c: Out(1)
    seg_d: Out(1)
    seg_e: Out(1)
    seg_f: Out(1)
    seg_g: Out(1)

    def elaborate(self, platform):
        m = Module()

        output = Signal(7)

        with m.Switch(self.bcd):
            with m.Case(0x0): m.d.comb += output.eq(0b1111110)
            with m.Case(0x1): m.d.comb += output.eq(0b0110000)
            with m.Case(0x2): m.d.comb += output.eq(0b1101101)
            with m.Case(0x3): m.d.comb += output.eq(0b1111001)
            with m.Case(0x4): m.d.comb += output.eq(0b0110011)
            with m.Case(0x5): m.d.comb += output.eq(0b1011011)
            with m.Case(0x6): m.d.comb += output.eq(0b1011111)
            with m.Case(0x7): m.d.comb += output.eq(0b1110000)
            with m.Case(0x8): m.d.comb += output.eq(0b1111111)
            with m.Case(0x9): m.d.comb += output.eq(0b1111011)
            with m.Case(0xA): m.d.comb += output.eq(0b1110111)
            with m.Case(0xB): m.d.comb += output.eq(0b0011111)
            with m.Case(0xC): m.d.comb += output.eq(0b1001110)
            with m.Case(0xD): m.d.comb += output.eq(0b0111101)
            with m.Case(0xE): m.d.comb += output.eq(0b1001111)
            with m.Case(0xF): m.d.comb += output.eq(0b1000111)
            with m.Default(): m.d.comb += output.eq(0b0000000)

        m.d.comb += Cat([self.seg_g, self.seg_f, self.seg_e, self.seg_d,
            self.seg_c, self.seg_b, self.seg_a]).eq(output)

        return m

