"""
Functions that utilize NTD data to estimate fuel efficiency of different public transit
modes in a given year and area code.
"""

import emcommon.logger as Logger
import emcommon.metrics.footprint.util as util
from emcommon.metrics.footprint.ntd_data_by_year import ntd_data, uace_zip_maps

fuel_types = ['Gasoline', 'Diesel', 'LPG', 'CNG', 'Hydrogen', 'Electric', 'Other']

def weighted_mean(values, weights):
    w_sum = sum(weights)
    return sum([v * w / w_sum for v, w in zip(values, weights)])

def get_uace_by_zipcode(zipcode: str, year: int) -> str:
    year = str(year - year % 10)
    for uace in uace_zip_maps[year]:
        if zipcode in uace_zip_maps[year][uace]:
            return uace
    Logger.log_warn(f"UACE code not found for zipcode {zipcode} in year {year}")
    return None

def get_intensities_for_trip(trip, modes):
    year = util.year_of_trip(trip)
    uace_code = get_uace_by_zipcode(trip["start_confirmed_place"]["zipcode"], year)
    return get_intensities_for_year_and_uace(year, uace_code, modes)

def get_intensities_for_year_and_uace(year: int, uace: str, modes: list[str]):
    """
    Returns the estimated energy intensity by fuel type across the given modes in the urban area of the given trip.
    :param trip: The trip to get the data for, e.g. {"year": "2022", "distance": 1000, "start_confirmed_place": {"zipcode": "45221"}}
    :param modes: The NTD modes to get the data for, e.g. ["MB","CB"] (https://www.transit.dot.gov/ntd/national-transit-database-ntd-glossary)
    :returns: A dictionary of energy intensities by fuel type, with weights, e.g. {"gasoline": { "wh_per_km": 1000, "weight": 0.5 }, "diesel": { "wh_per_km": 2000, "weight": 0.5 }, "overall": { "wh_per_km": 1500, "weight": 1.0 } }
    """
    Logger.log_debug(f"Getting mode footprint for transit modes {modes} in year {year} and UACE {uace}")

    footprint = {}
    metadata = {
        "source": "NTD",
        "is_provisional": False,
        "year": year,
        "requested_year": year,
        "uace_code": uace,
        "modes": modes,
    }

    year_str = str(year)
    if (year_str not in ntd_data):
        year_str = str(util.find_closest_available_year(year, ntd_data.keys()))
        metadata["is_provisional"] = True
        metadata["year"] = year_str
        Logger.log_warn(f"NTD data not available for year {year}; using closest available year {year_str}")

    agency_mode_fueltypes = []
    for entry in ntd_data[year_str]:
        if entry["UACE Code"] == uace and entry["Mode"] in modes:
            Logger.log_debug(f"NTD ID: {entry['NTD ID']}; "
                           + f"Mode = {entry['Mode']}; "
                           + f"pkm = {entry['Passenger km']}; "
                           + f"all_fuels_km = {entry['All Fuels (km)']}; "
                           + f"average_passengers = {entry['Average Passengers']}")
            pkm = entry['Passenger km']
            all_fuels_km = entry['All Fuels (km)']
            average_passengers = entry['Average Passengers']
            for fuel_type in fuel_types:
                km_value = entry.get(f"{fuel_type} (km)", 0)
                wh_per_km_value = entry.get(f"{fuel_type} (Wh/km)", 0)
                if km_value and wh_per_km_value:
                    agency_mode_fueltypes.append({
                        "ntd_id": entry['NTD ID'],
                        "mode": entry['Mode'],
                        "fuel_type": fuel_type,
                        "pkm": km_value / all_fuels_km * pkm,
                        "wh_per_km": wh_per_km_value / average_passengers
                    })

    total_pkm = sum([entry['pkm'] for entry in agency_mode_fueltypes])
    for entry in agency_mode_fueltypes:
        entry['weight'] = entry['pkm'] / total_pkm
    Logger.log_debug(f"agency_mode_fueltypes = {agency_mode_fueltypes}")

    for fuel_type in fuel_types:
        fuel_type_entries = [entry for entry in agency_mode_fueltypes
                             if entry['fuel_type'] == fuel_type]
        if not fuel_type_entries:
            continue
        wh_per_km_values = [entry['wh_per_km'] for entry in fuel_type_entries]
        weights = [entry['weight'] for entry in fuel_type_entries]
        Logger.log_debug(f"fuel_type = {fuel_type}; wh_per_km_values = {wh_per_km_values}; weights = {weights}")
        fuel_type = fuel_type.lower()
        footprint[fuel_type] = {
            "wh_per_km": weighted_mean(wh_per_km_values, weights),
            "weight": sum(weights)
        }

    # take the overall weighted average between fuel types
    wh_per_km_values = [entry['wh_per_km'] for entry in agency_mode_fueltypes]
    weights = [entry['weight'] for entry in agency_mode_fueltypes]
    footprint['overall'] = {
        "wh_per_km": weighted_mean(wh_per_km_values, weights),
        "weight": sum(weights)
    }

    Logger.log_info(f"footprint = {footprint}; metadata = {metadata}")
    return (footprint, metadata)
