from sim_modules.preload import Preload

def get_simulator_module(module_name, simulator, module_settings):
    # Insert call to create specific simulator module here
    if (module_name == 'preload-predictor'):
        return Preload(module_name, module_settings, simulator)
    else:
        print("No relative module is created")