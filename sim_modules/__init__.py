from sim_modules.ChromePreloader import ChromePreloader
from sim_interface import SimModuleType

def get_simulator_module(module_name, simulator, module_settings):
    # Insert call to create specific simulator module here
    if module_name == "chrome-preload-predictor":
        return ChromePreloader(module_name, SimModuleType.CHROME_PRELOAD_PREDICTOR, simulator)
    else:
        print("No relative module is created")
