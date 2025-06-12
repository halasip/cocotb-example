# 
import os
import sys
from pathlib import Path

import logging
import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotbext.uart import UartSource, UartSink

# cocotb decorator indicating a test to run with simulator.
# multiple tests may be included in the same python module (file)
@cocotb.test()
async def my_test(dut):

    uart_driver = UartSource(dut.rx_uart_serial_in, baud=1000000, bits=8)
    # uart_sink   = UartSink(dut.rx_uart_serial_in, baud=1000000, bits=8)
    uart_sink   = UartSink(dut.tx_uart_serial_out, baud=1000000, bits=8)
    uart_driver.log.setLevel(logging.DEBUG)
    await prerun(dut)

    TestValues = [1, 2, 3, 4]
    ExpectedValues = [5, 6, 7, 8]
    for Test, Expected in zip(TestValues, ExpectedValues):
        print(Test, Expected)
        expected_result = Expected
        test_value = expected_result**2

        await uart_driver.write(test_value.to_bytes(1, "little")) 
        ##### read command
        await uart_driver.wait()
        ##### print ByteArray as bytes
        result = await uart_sink.read(count=1)
        result = int.from_bytes(result, "little")
        print(bytes(result))
        print(bytes(expected_result))
        assert result == expected_result
    
    await Timer(100, 'ns')

    await postrun(dut)

    pass

async def prerun(dut):
    """Initialize the DUT (Device Under Test) with a clock and reset."""
    # Create a clock signal with a period of 10 time units
    c = Clock(dut.clk, 100, 'ns')
    await cocotb.start(c.start())

    dut.reset.value = 1
    await cocotb.triggers.ClockCycles(dut.clk, 5, rising=True)
    dut.reset.value = 0
    await cocotb.triggers.ClockCycles(dut.clk, 2, rising=True)

async def postrun(dut):
    await cocotb.triggers.ClockCycles(dut.clk, 5, rising=True)
    dut.reset.value = 1
    await cocotb.triggers.ClockCycles(dut.clk, 2, rising=True)



def simulation_runner():
    """Simulate the adder example using the Python runner.

    This file can be run directly or via pytest discovery.
    """
    simulator_program = "ghdl"
    WaveformOptionVcd = "--vcd=waveforms.vcd"

    proj_path = Path(__file__).resolve().parent.parent

    vhdl_sources = []
    vhdl_sources += [proj_path / "hdl" / "RT2024MySystemTop.vhd"]
    vhdl_sources += [proj_path / "hdl" / "sqrt_conv.vhd"]
    vhdl_sources += [proj_path / "hdl" / "uart_rx.vhd"]
    vhdl_sources += [proj_path / "hdl" / "uart_tx.vhd"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(simulator_program)
	
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="rt2024mysystemtop",
        always=True,
    )
	
    runner.test(hdl_toplevel="rt2024mysystemtop", 
				test_module="Lab04_FunctionAndDrivers",
				plusargs=[WaveformOptionVcd, "--ieee-asserts=disable"])


if __name__ == "__main__":
    simulation_runner()
