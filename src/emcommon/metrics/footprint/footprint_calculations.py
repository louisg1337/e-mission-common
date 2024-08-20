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
def get_egrid_carbon_intensity(year: int, coords: list[float, float] | None = None) -> float:
  """
  Returns the estimated carbon intensity of the electricity grid at the given coordinates for the
  given year (units in kg CO2e per MWh).

  :param year: The year as int, e.g. 2022
  :param coords: The coordinates as [lon, lat], e.g. [-84.52, 39.13]
  """
  metadata = {
    "source": "eGRID",
    "is_provisional": False,
    "year": year,
    "requested_year": year,
    "coords": coords,
    "egrid_region": None,
  }
  if str(year) not in egrid_data:
      year = util.find_closest_available_year(year, egrid_data.keys())
      metadata['year'] = year
      metadata['is_provisional'] = True
      Logger.log_warn(f"eGRID data not available for year {metadata['requested_year']}; "
                    + f"Using closest available year {metadata['year']}")
  egrid_data_for_year = egrid_data[str(year)]
  if coords is not None:
    region_feature = util.get_feature_containing_point(coords, egrid_regions[year])
    if region_feature is not None:
      metadata['egrid_region'] = region_feature['properties']['Name']
  if metadata['egrid_region'] is None:
    if coords is not None:
      Logger.log_warn(f"eGRID region not found for coords {coords} in year {year}. Using national average.")
    else:
      Logger.log_debug(f"Coords not given for eGRID lookup in year {year}. Using national average.")
      # use national average
      kg_per_kwh = egrid_data_for_year['national_kg_per_mwh']
      return None
  else:
    kg_per_kwh = egrid_data_for_year['regions_kg_per_mwh'][metadata['egrid_region']]
  return (kg_per_kwh, metadata)
# __pragma__('nojsiter')


def calc_footprint_for_trip(trip, mode_label_option):
  """
  Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
  """
  Logger.log_debug('Getting footprint for trip: ' + str(trip) +
                   ', with mode option: ' + str(mode_label_option))
  metadata = {}
  distance = trip['distance']
  rich_mode = emcdb.get_rich_mode(mode_label_option)
  mode_footprint = dict(rich_mode['footprint'])
  if 'transit' in mode_footprint:
    [mode_footprint, metadata] = transit.get_intensities_for_trip(trip, mode_footprint['transit'])
  kwh_total = 0
  kg_co2_total = 0
  for fuel_type, fuel_type_footprint in mode_footprint.items():
    # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
    kwh = (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
    if fuel_type in util.FUELS_KG_CO2_PER_KWH:
      Logger.log_debug('Using default carbon intensity for fuel type: ' + fuel_type)
      kg_co2 = kwh * util.FUELS_KG_CO2_PER_KWH[fuel_type]
    elif fuel_type == 'electric':
      Logger.log_debug('Using eGRID carbon intensity for electric')
      year = util.year_of_trip(trip)
      coords = trip['start_loc']['coordinates']
      [kg_per_kwh, metadata] = get_egrid_carbon_intensity(year, coords)
      kg_co2 = kwh * kg_per_kwh
    else:
      Logger.log_warn('Unknown fuel type: ' + fuel_type)
      continue
    kwh_total += kwh
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
    "metadata": metadata,
  }
