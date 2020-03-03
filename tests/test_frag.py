import os
import shutil
import pele_platform.constants.constants as cs
import pele_platform.main as main

test_path = os.path.join(cs.DIR, "Examples")


FRAG_ARGS = [os.path.join(test_path, "frag/input.yaml")]
FRAG_SIM_ARGS = [os.path.join(test_path, "frag/input_sim.yaml")]


def test_frag(ext_args=FRAG_ARGS, output="1w7h_preparation_structure_2w_aminoC1N1"):
    if os.path.exists(output):
        shutil.rmtree(output)
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.Launcher(arguments).launch()

def test_frag_sim(ext_args=FRAG_SIM_ARGS, output="1w7h_preparation_structure_2w_aminoC1N1"):
    if os.path.exists(output):
        shutil.rmtree(output)
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.Launcher(arguments).launch()

