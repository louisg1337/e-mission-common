import emcommon.metrics.footprint.transit_calculations as jack_transit_calculations
import emcommon.metrics.footprint.louis_transit_calculations as louis_transit_calculations
from emcommon.diary.base_modes import BASE_MODES

# print(louis_transit_calculations.get_intensities(2022, "16264", ["MB", "RB", "CB"]))

cities = [
    "63217", # New York
    "16264", # Chicago
    "32167", # GAinesville
    "16885", # Cincinnati
    "09271", # Boston
    "40429", # Houston
    "03817", # Atlanta
]

for uace in cities:
    print('---- City: ' + uace + ' ----')
    for mode in BASE_MODES:
        if 'footprint' not in BASE_MODES[mode] or 'transit' not in BASE_MODES[mode]['footprint']:
            continue
        print('Mode:', mode)
        print(jack_transit_calculations.get_intensities(
            2022,
            uace,
            BASE_MODES[mode]['footprint']['transit']
        )[0]['overall']['wh_per_km'])
        intensities = louis_transit_calculations.get_intensities(
            2022,
            uace,
        BASE_MODES[mode]['footprint']['transit'])
        print(intensities['overall']['wh_per_km'])
