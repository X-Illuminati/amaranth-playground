from amaranth import *
from amaranth.build import *
from seven_seg_disp import SevenSegmentDisp
from lfsr import LFSRDynamic

class LFSRExplorer(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        m.domains.onehz = cd_onehz = ClockDomain(local=True)
        m.submodules.sevenseg = sevenseg = SevenSegmentDisp()
        m.submodules.lfsr = lfsr = DomainRenamer("onehz")(LFSRDynamic())

        seg_pins = platform.request("seven_seg")
        dipsw_pins = platform.request("dipswitch")

        # set up a timer to slow the processing to 1 Hz
        half_freq = int(platform.default_clk_frequency // 2)
        timer = Signal(range(half_freq + 1))
        slowclock = Signal(1)

        with m.If(timer == half_freq):
            m.d.sync += slowclock.eq(~slowclock)
            m.d.sync += timer.eq(0)
        with m.Else():
            m.d.sync += timer.eq(timer + 1)
        m.d.comb += cd_onehz.clk.eq(slowclock)
        m.d.comb += seg_pins.dp.o.eq(slowclock)

        lfsrnibble = Signal(4)

        # map the lfsr inputs and outputs
        m.d.comb += [
            lfsr.taps.eq(dipsw_pins.i),
            lfsrnibble.eq(lfsr.out)
        ]

        # map the sevenseg module's inputs and output
        m.d.comb += [
            sevenseg.bcd.eq(lfsrnibble),
            seg_pins.seg_a.o.eq(sevenseg.seg_a),
            seg_pins.seg_b.o.eq(sevenseg.seg_b),
            seg_pins.seg_c.o.eq(sevenseg.seg_c),
            seg_pins.seg_d.o.eq(sevenseg.seg_d),
            seg_pins.seg_e.o.eq(sevenseg.seg_e),
            seg_pins.seg_f.o.eq(sevenseg.seg_f),
            seg_pins.seg_g.o.eq(sevenseg.seg_g),
        ]

        return m

from amaranth_boards.icestick import ICEStickPlatform
plat = ICEStickPlatform()
seven_seg = [
    Resource("seven_seg", 0,
             Subsignal("seg_b", PinsN("3", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_g", PinsN("4", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_c", PinsN("5", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_d", PinsN("6", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_a", PinsN("7", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_f", PinsN("8", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("seg_e", PinsN("9", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")),
             Subsignal("dp", PinsN("10", dir="o", conn=("j", 1)), Attrs(IO_STANDARD="SB_LVCMOS33")))
]
dipswitch = [
    Resource("dipswitch", 0, Pins("10 9 8 7 6 5 4 3", dir="i", conn=("j", 3)))
]
plat.add_resources(seven_seg)
plat.add_resources(dipswitch)
plat.build(LFSRExplorer(), do_program=True)

