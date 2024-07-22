"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

# https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
KG_CO2_PER_GALLON_GASOLINE = 8.89
KG_CO2_PER_GALLON_DIESEL = 10.18
KG_CO2_PER_GALLON_BIODIESEL = KG_CO2_PER_GALLON_DIESEL * .26 # https://afdc.energy.gov/fuels/biodiesel-benefits
KG_CO2_PER_GALLON_LPG = 5.75 # https://www.eia.gov/environment/emissions/co2_vol_mass.php
KG_CO2_PER_GALLON_CNG = KG_CO2_PER_GALLON_GASOLINE * 1.22 # https://www.ctc-n.org/technology-library/vehicle-and-fuel-technologies/compressed-natural-gas-cng-fuel
KG_CO2_PER_KG_HYDROGEN = 0 
KG_CO2_PER_KWH_ELECTRICITY = 0.5 # Figure out way to integrate this with eGrid work

DIESEL_GGE = 1.136 # from energy.gov
KWH_PER_GALLON_GASOLINE = 33.7 # from the EPA, used as the basis for MPGe
KWH_PER_GALLON_DIESEL = KWH_PER_GALLON_GASOLINE * 1.14
# GGE constants found from https://epact.energy.gov/fuel-conversion-factors
KWH_PER_GALLON_BIODIESEL = KWH_PER_GALLON_GASOLINE * 1.05 
KWH_PER_GALLON_LPG = KWH_PER_GALLON_GASOLINE * .74
KWH_PER_GALLON_CNG = KWH_PER_GALLON_GASOLINE * .26
KWH_PER_KG_HYDROGEN = KWH_PER_GALLON_GASOLINE * 1.00

KG_CO2_PER_KWH_GASOLINE = KG_CO2_PER_GALLON_GASOLINE / KWH_PER_GALLON_GASOLINE
KG_CO2_PER_KWH_DIESEL = KG_CO2_PER_GALLON_DIESEL / KWH_PER_GALLON_DIESEL

MI_PER_KM = 0.621371

def mpge_to_wh_per_km(mpge: float) -> float:
  """
  Convert miles per gallon of gasoline equivalent (MPGe) to watt-hours per kilometer.
  e.g. mpge_to_wh_per_km(100) -> 209.40202700000003
  """
  return MI_PER_KM / mpge * KWH_PER_GALLON_GASOLINE * 1000

print(mpge_to_wh_per_km(22))

def grid_emission_rate_for_trip(trip):
  # TODO
  pass

def calc_footprint_for_trip(trip, mode_footprint):
  """
  Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
  """
  distance = trip['distance']
  kwh_total = 0
  kg_co2_total = 0
  for fuel_type, fuel_type_footprint in mode_footprint.items():
    # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
    kwh = (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
    if fuel_type == 'electric':
      kg_per_kwh = grid_emission_rate_for_trip(trip)
      kg_co2 = kwh * kg_per_kwh
    if fuel_type == 'gasoline':
      kg_co2 = kwh * KG_CO2_PER_KWH_GASOLINE
    if fuel_type == 'diesel':
      kg_co2 = kwh * KG_CO2_PER_KWH_DIESEL
    kwh_energy += kwh
    kg_co2_total += kg_co2

  return {
    'kwh': kwh_total,
    'kg_co2': kg_co2_total
  }
