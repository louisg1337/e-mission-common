from logger import log_debug

km_per_mile = 1.609344
kwh_per_gallon = 33.7
default_car_footprint = 278 / 1609
default_mpg = 8.91 / (1.6093 * default_car_footprint)  # Should be roughly 32


def get_carbon_mode_map():
    log_debug("Returning mode map for carbon calculations")
    # using conversion: 8.91 kg CO2 for one gallon
    # must convert Mpg -> Km, factor of 1000 in denom for g -> kg conversion
    default_km_per_gallon = default_mpg * km_per_mile
    car_footprint = (1 / default_km_per_gallon) * 8.91
    modeMap = {
        'walking': 0,
        'running': 0,
        'cycling': 0,
        'mixed': 0,
        'bus_short': 267.0 / 1609,
        'bus_long': 267.0 / 1609,
        'train_short': 92.0 / 1609,
        'train_long': 92.0 / 1609,
        'car_short': car_footprint,
        'car_long': car_footprint,
        'air_short': 217.0 / 1609,
        'air_long': 217.0 / 1609,
    }
    return modeMap
