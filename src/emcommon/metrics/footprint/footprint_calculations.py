"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

import emcommon.logger as Logger
from emcommon.metrics.footprint.egrid_carbon_by_year import egrid_data
import emcommon.diary.base_modes as emcdb
import emcommon.metrics.footprint.transit_calculations as transit
import emcommon.metrics.footprint.util as util

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


def calc_footprint_for_trip(trip, mode_label_option):
  """
  Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
  """
  distance = trip['distance']
  rich_mode = emcdb.get_rich_mode(mode_label_option)
  mode_footprint = rich_mode['footprint']
  if 'transit' in mode_footprint:
    mode_footprint = transit.get_mode_footprint_for_transit(trip, mode_footprint['transit'])
  kwh_total = 0
  kg_co2_total = 0
  for fuel_type, fuel_type_footprint in mode_footprint.items():
    # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
    kwh = (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
    if fuel_type in FUELS_KG_CO2_PER_KWH:
      kg_co2 = kwh * FUELS_KG_CO2_PER_KWH[fuel_type]
    elif fuel_type == 'electric':
      year = trip['start_fmt_time'].split('-')[0]
      zipcode = trip['start_confirmed_place']['zipcode'] # TODO
      kg_per_kwh = get_egrid_carbon_intensity(year, zipcode)
      kg_co2 = kwh * kg_per_kwh
    else:
      Logger.log_error('Unknown fuel type: ' + fuel_type)
      continue
    kwh_energy += kwh
    kg_co2_total += kg_co2

  # Divide by number of passengers, if specified:
  # Some modes (air, transit modes) already account for this; the given footprints are per
  # passenger-km and 'passengers' is not defined.
  # Other modes (car, carpool) have a flexible number of passengers. The footprints are
  # per vehicle-km. Dividing by 'passengers' gives the footprint per passenger-km.
  passengers = mode_label_option['passengers'] if 'passengers' in mode_label_option else 1
  return {
    'kwh': kwh_total / passengers,
    'kg_co2': kg_co2_total / passengers,
  }
