from __future__ import annotations # __: skip
import emcommon.logger as Logger
# from util import memoize

km_per_mile = 1.609344
kwh_per_gallon = 33.7
default_car_footprint = 278 / 1609
default_mpg = 8.91 / (1.6093 * default_car_footprint)  # Should be roughly 32

# using conversion: 8.91 kg CO2 for one gallon
mpg_to_co2_per_km = lambda mpg: (1 / (mpg * km_per_mile)) * 8.91

# To my knowledge, this is not used anywhere, because we always use the configurable label_options
# for the carbon mode map. Kept here for reference until I can verify it won't be used.
default_carbon_mode_map = {
    'walking': 0,
    'running': 0,
    'cycling': 0,
    'mixed': 0,
    'bus_short': 267.0 / 1609,
    'bus_long': 267.0 / 1609,
    'train_short': 92.0 / 1609,
    'train_long': 92.0 / 1609,
    'car_short': mpg_to_co2_per_km(default_mpg),
    'car_long': mpg_to_co2_per_km(default_mpg),
    'air_short': 217.0 / 1609,
    'air_long': 217.0 / 1609,
}

# @memoize
def get_carbon_mode_map(label_options: dict[str, any]) -> dict[str, float]:
    """
    :param label_options: label options dict (from dynamic config 'label_options')
    :return: a dict of modes to their footprints (unit of CO2 per km)
    """
    mode_options = label_options['MODE']
    mode_co2_entries = {}
    range_limited_motorized = None
    for opt in mode_options:
        if 'range_limit_km' in opt:
            if range_limited_motorized:
                Logger.log_debug(f'Found two range limited motorized options: {range_limited_motorized} and {opt}')
            range_limited_motorized = opt
            Logger.log_debug(f'Found range limited motorized mode - {range_limited_motorized}')
        if 'kgCo2PerKm' in opt:
            mode_co2_entries[opt['value']] = opt['kgCo2PerKm']
    return mode_co2_entries

# @memoize
def highest_carbon_mode(label_options: dict[str, any]) -> str:
    """
    :param label_options: label options dict (from dynamic config 'label_options')
    :return: mode with the highest carbon intensity
    """
    mode_co2_entries = get_carbon_mode_map(label_options)
    return max(mode_co2_entries, key=mode_co2_entries.get)

# @memoize
def carbon_summary_by_mode(composite_trips: list, label_options: dict[str, any]):
    """
    :param composite_trips: list of composite trips
    :param label_options: label options dict (from dynamic config 'label_options')
    :return: a dict of modes to the total carbon footprint using that mode
    """
    mode_to_distance_map = distance_summary_by_mode(composite_trips)
    mode_to_carbon_map = get_carbon_mode_map(label_options)
    carbon_summary = {}
    for mode, distance in mode_to_distance_map.items():
        carbon_summary[mode] = distance * mode_to_carbon_map[mode]
    return carbon_summary
