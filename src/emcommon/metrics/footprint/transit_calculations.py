"""
Functions that utilize NTD data to estimate fuel efficiency of different public transit
modes in a given year and area code.
"""

import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import json
from collections import defaultdict

# Import data
with open('ntd_fuel_energy.json', 'r') as file:
    fuel_energy_data = json.load(file)

with open("ntd_service_pmt.json", 'r') as file:
    service_pmt_data = json.load(file)

factors = {
    "Gasoline": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_GASOLINE},
    "Diesel": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_DIESEL},
    "Bio-Diesel": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_BIODIESEL},
    "Liquefied Petroleum Gas": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_LPG},
    "Compressed Natural Gas": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_CNG},
    "Hydrogen": {"kWh_per_unit":  footprint_calculations.KWH_PER_KG_HYDROGEN},
    "Electric Propulsion": {"kWh_per_unit": 1},
    "Electric Battery": {"kWh_per_unit": 1},
    "Other Fuel": {"kWh_per_unit":  footprint_calculations.KWH_PER_GALLON_GASOLINE},
}

mode_conversion = {
    "Bus": ["CB", "MB", "RB", "TB"],
    "Train": ["LR", "CC", "SR", "TR", "CR", "HR", "MG", "YR"],
    "": []
}

def get_ntd_ids_by_uace(code, year):
    '''
    Given an UACE code, find all the NTD ids within it. Necessary because the PMT data
    only has NTD ids, so this helps us bridge the gap between Fuel + Energy data and Service (PMT) data.
    '''
    ids = set()
    for row in fuel_energy_data[year][code]:
        ids.add(str(row["NTD ID"]))
    return ids

def average_passengers(code, modes, year):
    '''
    Calculate the average number of passengers using public transit given the constraints of UACE code, modes, and year.
    To do this we do the following steps:

    1) Gather all NTD ids in a given UACE code. 
       - This is necessary as the Service/PMT data uses NTD ids instead of UACE codes, so we must convert our UACE code into its corresponding NTD ids that make it up. 
    2) Search through each NTD id (aka agency) in our UACE code and see if it has data on our modes we are searching for.
    3) If the agency has information on the modes we are looking for, add it to our aggregate_modes array.
    4) Sum up all the instances of "Total Miles" and "PMT" in all the mode data we found.
    '''
    # Find all NTD id's by UACE code
    ntd_ids = get_ntd_ids_by_uace(code, year)
    # Goal is to collect all data about each mode 
    aggregate_modes = []
    # Search through each ntd_id in a given UACE code
    for ntd_id in ntd_ids:
        # Get the agency based on the ntd_id, if it doesn't exist we can skip
        agency = service_pmt_data[year].get(ntd_id, None)
        if agency == None: continue
        # Given an agency with an ntd_id in our UACE code, search through the agency's modes for the ones we are looking for
        for mode in agency:
            # If we find a mode within the agency we are looking for, add to our aggregate data.
            if mode in modes:
                aggregate_modes.append(agency[mode])
    # Sum up all the miles
    total_miles = sum(
        (int(mode["Vehicle Revenue Miles"].replace(",", "")) + int(mode["Train Revenue Miles"].replace(",", "")) )
        # (int(mode["Total Vehicle Miles"].replace(",", "")) + int(mode["Total Train Miles"].replace(",", "")) )
        for modes in aggregate_modes
        for mode in modes
    )
    # Sum up all the PMTs
    total_pmt = sum(
        int(mode["PMT"].replace(",", ""))
        for modes in aggregate_modes
        for mode in modes
    )
    # Convert to km
    total_kms =  total_miles * 1.60934
    total_pkt = total_pmt * 1.60934
    avg = 0
    if total_kms != 0:
        avg = float(total_pkt) / float(total_kms)
    return (avg, aggregate_modes)

def aggregate_fuel_data(code, modes, year, fields, get_factor):
    '''
    Aggregate and sum all fields provided in a given year, area code, and modes. Then applies a constant
    factor to the item which is obtained by passing in a "field_name" to get_factor().
    '''
    # Store all the totals in one big dictionary
    totals = defaultdict(int)
    aggregate_data = []
    # Look through every entry in our fuel data based on year and area code
    for entry in fuel_energy_data[year][code]:
        # Only care about modes that we have specified
        if entry["Mode"] in modes:
            # Create new trimmed down object for all the fields we care about
            new_entry = {"NTD ID": entry["NTD ID"], "Mode": entry["Mode"]}
            # Keep track of total that all fields sum up to
            total_value = 0
            # Extract and sum the data for each field
            for field in fields:
                field_num = int(entry[field].replace(",",""))
                total_value += field_num
                # Copy field we want into our new trimmed object
                new_entry[field] = field_num
                # Trim the name e.g. Gasoline (Miles) --> Gasoline
                field_name = field.split(" (").pop(0)
                # Put the data in our totals
                totals[field_name] += field_num * get_factor(field_name)
            # Add in the total_value
            new_entry["Total"] = total_value
            # Add filtered dictionary to aggregate_data
            aggregate_data.append(new_entry)
        
    return (totals, aggregate_data)

def aggregate_total_whs(code, modes, year):
    '''
    Finds total kWh in a given year, area code, and between modes 
    '''
    fields = ["Diesel (gal)","Gasoline (gal)","Liquefied Petroleum Gas (gal equivalent)","Compressed Natural Gas (gal equivalent)","Other Fuel (gal/gal equivalent)","Electric Propulsion (kWh)","Electric Battery (kWh)"]
    if int(year) >= 2022:
        fields.append("Hydrogen (kg)")
    get_factor = lambda factor: factors[factor]["kWh_per_unit"] * 1000
    (total_whs, aggregate_gallons_data) = aggregate_fuel_data(code, modes, year, fields, get_factor)
    return (total_whs, aggregate_gallons_data)

def aggregate_total_kms(code, modes, year):
    '''
    Finds total KMs in a given year, area code, and between modes
    '''
    fields = ["Diesel (miles)","Gasoline (miles)","Liquefied Petroleum Gas (miles)","Compressed Natural Gas (miles)","Other Fuel (miles)","Electric Propulsion (miles)","Electric Battery (miles)"]
    if int(year) >= 2022:
        fields.append("Hydrogen (miles)")
    get_factor = lambda _: 1.60934
    (total_kms, aggregate_miles_data) = aggregate_fuel_data(code, modes, year, fields, get_factor)
    return (total_kms, aggregate_miles_data)

def calculate_weights(aggregate_gallons_data, aggregate_modes):
    '''
    Calculate the weights of each fuel type. The calculations of how to get it are described in this github issue comment:
    https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2252070684
    '''
    refactored = defaultdict(dict)
    # First thing we want to do is to combine the aggregate_modes into the ntd_id: { mode1: {}, mode2:{} } format
    for modes in aggregate_modes:
        for mode in modes:
            ntd_id = mode['NTD ID']
            mode_type = mode['Mode']
            pkt = int(mode["PMT"].replace(",","")) * 1.60934
            if ntd_id in refactored and mode_type in refactored[ntd_id]:
                # Check to see if mode already exists within ntd_id, if it does then add the values
                refactored[ntd_id][mode_type]["PKT"] += pkt
            else:
                # If mode doesn't exist, just add it in
                refactored[ntd_id][mode_type] = {"PKT": pkt}

    # Now we want to add all the gallon data into refactored
    for agency in aggregate_gallons_data:
        ntd_id = agency["NTD ID"]
        mode = agency["Mode"]
        # Add in the gallon data, and remove NTD ID + Mode because we already store that info
        refactored[ntd_id][mode].update(agency)
        refactored[ntd_id][mode].pop("NTD ID")
        refactored[ntd_id][mode].pop("Mode")

    # Find the percentage of each fuel type used and add up total passenger km
    total_passenger_km = 0
    for agency in refactored:
        for mode in refactored[agency]:
            for field in refactored[agency][mode]:
                if field == "PKT":
                    # Add up total passenger kms 
                    total_passenger_km += refactored[agency][mode][field]
                elif field != "Total":
                    # Calculating averages for each fuel type within each mode
                    if refactored[agency][mode][field] != 0:
                        refactored[agency][mode][field] /= refactored[agency][mode]["Total"]

    # Calculate the weight by agency & mode based off of the PKT, and then adjust the percentages of the fuel types using that weight
    for agency in refactored:
        for mode in refactored[agency]:
            # Calculate the weight by passenger kilometers traveled
            refactored[agency][mode]["weight_by_pkt"] = refactored[agency][mode]["PKT"] / total_passenger_km
            for field in refactored[agency][mode]:
                if field != "weight_by_pkt" and field != "PKT" and field != "Total":
                    if refactored[agency][mode][field] != 0:
                        refactored[agency][mode][field] *= refactored[agency][mode]["weight_by_pkt"]

    fuel_type_weights = defaultdict(int)

    # Add up all the percentages of each fuel type
    for agency in refactored:
        for mode in refactored[agency]:
            for field in refactored[agency][mode]:
                if field != "weight_by_pkt" and field != "PKT" and field != "Total":
                    fuel_name = field.split(" (").pop(0)
                    fuel_type_weights[fuel_name] += refactored[agency][mode][field]

    return fuel_type_weights

def get_mode_footprint_for_transit(trip, modes):
    year = trip["year"]
    code = trip["code"]
    # Set a default value in case we get a KeyError somewhere and have to return something
    fuel_efficiencies = {"Diesel": {"wh_per_km": 1000, "weight": 1.0}}

    try:
        # Test to see if year and code exist
        _ = fuel_energy_data[year]
        _ = fuel_energy_data[year][code]

        # Get all the data we need to compute efficiencies, 
        (total_kms, aggregate_miles_data) = aggregate_total_kms(code, modes, year)
        (total_whs, aggregate_gallons_data) = aggregate_total_whs(code, modes, year)
        (average_number_passengers, aggregate_modes) = average_passengers(code, modes, year)
        weights = calculate_weights(aggregate_gallons_data, aggregate_modes)

    except KeyError as e:
        print(f"Key not found: {e}")
        return fuel_efficiencies

    for fuel in total_kms:
        wh_per_km = 0
        wh_per_km_passenger = 0
        if total_kms[fuel] != 0:
            wh_per_km = total_whs[fuel] / total_kms[fuel]
            wh_per_km_passenger = wh_per_km / average_number_passengers

        fuel_efficiencies[fuel] = {
            "wh_per_km": wh_per_km_passenger,
            "weight": weights[fuel]
        }

    print(average_number_passengers)    
    
    print(json.dumps(fuel_efficiencies, indent=4))


fake_trip = {
    "year": "2022",
    "distance": 1000,
    "code": "63217"
}
modes = ["MB","CB"]

get_mode_footprint_for_transit(fake_trip, modes)