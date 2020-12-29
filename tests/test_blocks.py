import glob
import os
import pytest
import shutil

from pele_platform import main
import pele_platform.Utilities.Parameters.pele_env as pv
import pele_platform.Errors.custom_errors as ce
from pele_platform.constants import constants as cs
import pele_platform.Utilities.BuildingBlocks.blocks as bb
from pele_platform.Utilities.BuildingBlocks.pipeline import Pipeline
from pele_platform.Utilities.BuildingBlocks.selection import Scatter6, LowestEnergy5, GMM, Clusters
import pele_platform.Checker.valid_flags as vf
import pele_platform.Utilities.Helpers.yaml_parser as yp
from . import test_adaptive as tk

test_path = os.path.join(cs.DIR, "Examples")

GPCR_lines = [
    '"type" : "epsilon"',
    '"iterations" : 50',
    '"peleSteps" : 8',
    '"conditions": [0.7, 0.4, 0.0]'
]

OutIn_lines = [
    '"type" : "inverselyProportional"',
    '"iterations" : 100',
    '"peleSteps" : 8',
    '"conditions": [1, 0.6, 0.0]'
]

GlobalExploration_lines = [
    '"type" : "inverselyProportional"',
    '"iterations" : 100',
    '"peleSteps" : 4',
    '"conditions": [1, 0.6, 0.0]'
]

InducedFitExhaustive_lines = [
    '"type" : "independent"',
    '"iterations" : 1',
    '"peleSteps" : 1000',
    '"conditions": [1, 0.6, 0.4, 0.0]'
]

InducedFitFast_lines = [
    '"type" : "inverselyProportional"',
    '"iterations" : 30',
    '"peleSteps" : 12',
    '"conditions": [1, 0.6, 0.4, 0.0]'
]

Rescoring_lines = [
    '"type" : "independent"',
    '"iterations" : 20',
    '"peleSteps" : 12',
    '"conditions": [1, 0.6, 0.4, 0.0]'
]

Scatter6_inputs = ['/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_1.1_BindingEnergy-107.584.pdb']

LowestEnergy5_inputs = [
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_1.1_BindingEnergy-107.584.pdb',
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_2.1_BindingEnergy-102.463.pdb',
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_1.2_BindingEnergy-99.0239.pdb',
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_2.4_BindingEnergy-97.3843.pdb',
]

GMM_inputs = [
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch1_trajectory_2.1_BindingEnergy-64.1978.pdb',
 
    
    
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_1.1_BindingEnergy-107.584.pdb',
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch1_trajectory_1.5_BindingEnergy-62.9806.pdb',
    '/home/agruzka/work_pele_platform/pele_platform/Examples/Blocks/mock_simulation/results/BestStructs/epoch0_trajectory_3.4_BindingEnergy-43.7304.pdb'
]

Clusters_inputs = [
    'cluster1_epoch0_trajectory_3.1_BindingEnergy-76.1823.pdb',
    'cluster4_epoch1_trajectory_1.1_BindingEnergy-65.8932.pdb',
    'cluster6_epoch0_trajectory_1.3_BindingEnergy-96.088.pdb',
    'cluster8_epoch0_trajectory_1.1_BindingEnergy-107.584.pdb'
]


@pytest.mark.parametrize("iterable", [([Scatter6, bb.Rescoring]), ([bb.GPCR, bb.Rescoring]), ([])])
def test_pipeline_checker(iterable):
    try:
        env = pv.EnviroBuilder()
        simulation_params = Pipeline(iterable, env).run()
    except ce.PipelineError:
        assert True
        return
    assert False


@pytest.mark.parametrize(("yaml", "package", "block", "expected"),
                         [("gpcr/input_defaults.yaml", "gpcr_orth", bb.GPCR, GPCR_lines),
                          ("global/input_defaults.yaml", "global", bb.GlobalExploration, GlobalExploration_lines),
                          ("out_in/input_default.yaml", "out_in", bb.OutIn, OutIn_lines),
                          ("induced_fit/input_exhaustive_defaults.yaml", "induced_fit_exhaustive", bb.InducedFitExhaustive,
                           InducedFitExhaustive_lines),
                          ("induced_fit/input_fast_defaults.yaml", "induced_fit_fast", bb.InducedFitFast,
                           InducedFitFast_lines),
                          ("rescoring/input_defaults.yaml", "rescoring", bb.Rescoring, Rescoring_lines)])
def test_simulation_blocks(yaml, package, block, expected):
    
    # get YamlParser ready
    yaml_file = os.path.join(test_path, yaml)
    yaml = yp.YamlParser(yaml_file, vf.VALID_FLAGS_PLATFORM)
    yaml.read()
    
    # create pele environment
    pele_env = pv.EnviroBuilder()
    pele_env.initial_args = yaml
    pele_env.initial_args.package = pele_env.package = package
    
    # run Building Block
    simulation_block = block(pele_env, "test_folder")
    params = simulation_block.run()
    
    directory = params.pele_dir
    errors = []
    errors = tk.check_file(directory, "adaptive.conf", expected, errors)
    assert not errors


@pytest.fixture
def mock_simulation_env():
    env = pv.EnviroBuilder()                                                                                                                                                            
    env.pele_dir = os.path.join(test_path, "Blocks/mock_simulation")                                                                                                                    
    env.output = "output"                                                                                                                                                               
    env.iterations = 2                                                                                                                                                                  
    env.pele_steps = 12                                                                                                                                                                 
    env.cpus = 5                                                                                                                                                                        
    env.be_column = 5                                                                                                                                                                   
    env.topology = None                                                                                                                                                                 
    env.logger = None                                                                                                                                                                   
    env.residue = "LIG"

    selection_path = os.path.join(os.path.dirname(env.pele_dir), "test_Selection")
    if os.path.exists(selection_path):
        shutil.rmtree(selection_path)
    return env


@pytest.mark.parametrize(("selection_block", "expected"), [(Scatter6, Scatter6_inputs), (LowestEnergy5, LowestEnergy5_inputs), (GMM, GMM_inputs), (Clusters, Clusters_inputs)])
def test_selection_blocks(mock_simulation_env, selection_block, expected):

    selection = selection_block(mock_simulation_env, "test_folder")
    selection.run()

    assert selection.inputs == expected


def test_workflow():
    yaml = os.path.join(test_path, "Blocks/input_workflow.yaml")
    output = main.run_platform(yaml)
    rescoring_params = output[-1]
    rescoring_output = os.path.join(rescoring_params.pele_dir, rescoring_params.output, "*/trajectory*.pdb")
    output_files = glob.glob(rescoring_output)
    
    assert os.path.exists(rescoring_params.pele_dir)
    assert output_files


def test_workflow_checker():
    yaml = os.path.join(test_path, "Blocks/input_wrong_workflow.yaml")
    try:
        output = main.run_platform(yaml)
    except ce.PipelineError:                                                                                                                                                            
        assert True                                                                                                                                                                     
        return 
    assert False
