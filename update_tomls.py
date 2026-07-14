import os
import toml

base_dir = r"c:\GITHUB\Python\caracterizar\config\default\tests"
toml_files = [
    "HP_4155B/MES_FILE.toml",
    "HP_4192A/CV.toml",
    "HP_4192A/CV_IV_external.toml",
    "HP_4192A/CV_IV_ring_external.toml",
    "HP_4192A/CW.toml",
    "Keithley_2410/IV_ring.toml",
    "Keithley_2470/IV.toml",
    "Keithley_2470/IV4.toml",
    "Keithley_2470/IV_ring.toml",
    "Keithley_4200/CV.toml",
    "Keithley_4200/CW.toml",
    "Keysight_B1500LAN/SOLARMEMS.toml",
    "Keysight_B1500LAN/Test.toml",
    "Keysight_E4990A/CV.toml",
    "Keysight_E4990A/CV_IV_external.toml",
    "Keysight_E4990A/CV_IV_ring_external.toml",
    "Keysight_E4990A/CV_nanusens.toml",
    "Keysight_E4990A/CV_RF_nanusens.toml",
    "Keysight_E4990A/CW.toml"
]

for f in toml_files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = toml.load(file)
        
        modified = False
        if "plot" in data:
            old_plot = data["plot"]
            new_plot = {}
            for k, v in old_plot.items():
                if k != k.upper():
                    new_plot[k.upper()] = v
                    modified = True
                else:
                    new_plot[k] = v
            data["plot"] = new_plot
            
        if "parameters" in data:
            if "DISPLAY_GRAPH" in data["parameters"]:
                # user said "prefiero conservar el show_plot", we can remove DISPLAY_GRAPH or leave it. 
                # Let's remove it so it's not confusing.
                del data["parameters"]["DISPLAY_GRAPH"]
                modified = True
        
        if modified:
            with open(path, 'w') as out:
                toml.dump(data, out)
            print(f"Updated keys to uppercase in {f}")

print("Done")
