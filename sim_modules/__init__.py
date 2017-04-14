from sim_modules.preload_predictor import Preload
from sim_modules.frequency_counter import FrequencyCounter
from sim_interface import SimModuleType


def get_simulator_module(module_name, simulator, module_settings):
    # Insert call to create specific simulator module here
    if module_name == "preload":
        return Preload(module_name, SimModuleType.PRELOAD_PREDICTOR, simulator, module_settings)
    elif module_name == "frequencycounter":
        return FrequencyCounter(module_name, SimModuleType.FREQUENCY_COUNTER, simulator, module_settings)
    else:
        print("No relative module is created")
