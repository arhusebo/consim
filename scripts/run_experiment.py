import argparse
from enum import Enum 
import inspect
import os
import sys
import importlib.util
import logging
sys.path.append("./src/") # won't work if run from other paths
from convsim import *

"""Run experiments and/or present results"""

logger = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
        "module",
        help="name of the module that contains experiments"
    )
parser.add_argument(
        "-n",
        "--name",
        nargs="*",
        default=[],
        help="name of the experiment to run"
    )
parser.add_argument(
        "-c",
        help="only present results",
        action="store_true"
    )
parser.add_argument(
        "-o",
        "--output-path",
        help="output path for experiment results",
        default="./results"
)


class State(Enum):
    EXPERIMENT = 1
    PRESENT = 2
    DONE = 3


def filter_classes(o):
    #if not inspect.isclass(o): return False
    if not issubclass(o, Experiment): return False


def run_experiment():
    args = parser.parse_args()
    logger.info(f"Selecting experiment(s) from module {args.module}...")

    spec = importlib.util.spec_from_file_location(
        "experiment", args.module)
    m = importlib.util.module_from_spec(spec)
    sys.modules["experiment"] = m
    spec.loader.exec_module(m)

    members = inspect.getmembers_static(
        m,
        lambda o: inspect.isclass(o) and\
            issubclass(o, Experiment) and\
            not o is Experiment)

    class_names, _ = zip(*members)

    queried_names = set(args.name)
    available_names = set(class_names)
    unidentified_names = queried_names.difference(available_names)
    selected_names = available_names.intersection(queried_names) 
    if len(unidentified_names) > 0:
        raise ValueError(
            f"Unrecognized experiment names: {', '.join(unidentified_names)}")
    else:
        logger.info(f"Selected experiments {', '.join(selected_names)}")
    
    state = State.PRESENT if args.c else State.EXPERIMENT
    while not state == State.DONE:
        for name, cls in members:
            if not os.path.exists(args.output_path):
                os.mkdir(args.output_path)
            
            fname = f"{name}.pkl"
            res_path = os.path.join(args.output_path, fname)

            if state == State.PRESENT:
                logger.info(f"Presenting experiment '{name}'")
                try:
                    res = ExperimentResults.load(res_path)
                    cls.present(res.data)
                except Exception as e:
                    print(e)
                    logger.warning(f"Could not present the results for experiment '{name}'")

            elif state == State.EXPERIMENT:
                logger.info(f"Running experiment '{name}'")
                try:
                    res = ExperimentResults.from_object(cls.run())
                    res.save(res_path)
                    logger.info(f"Experiment '{name}' terminated successfully")
                except Exception as e:
                    print(e)
                    logger.warning(f"Experiment '{name}' was skipped")

        if state == State.EXPERIMENT:
            state = State.PRESENT
        else:
            state = State.DONE
            logger.info("Finish")

if __name__ == "__main__":
    run_experiment()