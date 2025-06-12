# 
import os
import sys
from pathlib import Path

import cocotb # type: ignore
from cocotb.runner import get_runner # type: ignore
from cocotb.triggers import Timer # type: ignore

# Define your test here. See first lab or CodeSnippets.py 
# for decorator and other special Python kewords
@cocotb.test()
async def mytest(dut):
    # https://docs.cocotb.org/en/stable/triggers.html#cocotb.triggers.Timer
    # Do nothing for 100 ns
    # note there is a missing keyword before "Timer"
    await Timer(100, units='ns')
    pass
    
# Cocotb/GHDL runner. Use the first lab as template.
def simulation_runner():
    """Simulate the adder example using the Python runner.

    This file can be run directly or via pytest discovery.
    """
    hdl_toplevel_lang = "vhdl"
    simulator_program = "ghdl"
    TopModule = "???"

    proj_path = Path(__file__).resolve().parent.parent
    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "model"))
    sys.path.append(str(proj_path / "tests"))

    # Initial file list, empty
    vhdl_sources = []
    # Append file to list
    vhdl_sources += [proj_path / "hdl" / "sqrt_conv.vhd"]
    runner_args = [
        # "--ieee-asserts=disable",
        "--vcd=waveforms.vcd",
    ]

    runner = get_runner(simulator_program)
	
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="square_root",
        always=True,
    )
	
    runner.test(
        hdl_toplevel="square_root", 
		test_module="lab02_cocotb", # name of this python file.
		plusargs=runner_args,
    )


if __name__ == "__main__":
    simulation_runner()
