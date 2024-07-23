"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

import emcommon.logger as Logger
from emcommon.metrics.footprint.egrid_carbon_by_year import egrid_data

# https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
KG_CO2_PER_GALLON_GASOLINE = 8.89
KG_CO2_PER_GALLON_DIESEL = 10.18

DIESEL_GGE = 1.136 # from energy.gov
KWH_PER_GALLON_GASOLINE = 33.7 # from the EPA, used as the basis for MPGe
KWH_PER_GALLON_DIESEL = KWH_PER_GALLON_GASOLINE * 1.14

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

# __pragma__('jsiter')
def get_egrid_carbon_intensity(year: int, zipcode: str) -> float:
  """
  Returns the estimated carbon intensity of the electricity grid in the given zip code for the given year.
  (units in kg CO2e per MWh)
  :param year: The year to get the data for, e.g. 2022
  :param zipcode: The 5-digit zip code to get the data for; e.g. "45221" (Cincinnati), "02115" (Boston)
  """
  year = str(year)
  try:
    region = None
    for r in egrid_data[year]['regions_zips']:
      if zipcode in egrid_data[year]['regions_zips'][r]:
        region = r
        break
    return egrid_data[year]['regions_src2erta'][region]
  except KeyError:
    return None
# __pragma__('nojsiter')


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
      year = trip['start_fmt_time'].split('-')[0]
      zipcode = trip['start_confirmed_place']['zipcode'] # TODO
      kg_per_kwh = get_egrid_carbon_intensity(year, zipcode)
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
