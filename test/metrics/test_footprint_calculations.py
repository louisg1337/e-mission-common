import unittest

import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import emcommon.metrics.footprint.util as util

KG_PER_LB = 0.453592

# eGRID expected values (collected from https://www.epa.gov/egrid/data-explorer)
# "I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
# at the <eGRID subregion> level for <2022>."
EGRID_EXPECTED_LBS_PER_KWH = {
    'RFCW': 1005.90,
    'NWPP': 605.87,
}

class TestFootprintCalculations(unittest.TestCase):
    def test_egrid_intensity_cincinnati_2022(self):
        # Cincinnati, OH (RFCW region)
        coords = [-84.52, 39.13]
        (kg_per_kwh, metadata) = footprint_calculations.get_egrid_carbon_intensity(2022, coords)

        expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["RFCW"] * KG_PER_LB
        expected_metadata = {
            "data_sources": ["egrid2022"],
            "is_provisional": False,
            "requested_year": 2022,
            "egrid_coords": coords,
            "egrid_region": "RFCW",
        }
        self.assertAlmostEqual(kg_per_kwh, expected_kg_per_kwh, places=2)
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])

    def test_egrid_intensity_eagle_point_2023(self):
        # Eagle Point, OR (NWPP region)
        coords = [-122.83, 42.29]
        (kg_per_kwh, metadata) = footprint_calculations.get_egrid_carbon_intensity(2023, coords)

        expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["NWPP"] * KG_PER_LB
        expected_metadata = {
            "data_sources": ["egrid2022"],
            "is_provisional": True, # provisional; 2023 was requested but 2022 was used
            "requested_year": 2023,
            "egrid_coords": coords,
            "egrid_region": "NWPP",
        }
        self.assertAlmostEqual(kg_per_kwh, expected_kg_per_kwh, places=2)
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])

    def test_car_default_footprint(self):
        """
        1 km in a default CAR should consume 0.87 kWh and emit 0.23 kg CO2e.
        """
        fake_trip = {'distance': 1000}
        fake_mode = {'base_mode': 'CAR', 'passengers': 1}

        (footprint, metadata) = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)

        expected_footprint = {'kwh': 0.87, 'kg_co2': 0.23}
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

        # with 2 passengers, the footprint should be halved
        fake_mode['passengers'] = 2

        (footprint, metadata) = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)

        expected_footprint = {'kwh': 0.87 / 2, 'kg_co2': 0.23 / 2}
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

    def test_car_custom_footprint(self):
        """
        1 km in a custom CAR (wh/km = 100) should consume 0.1 kWh and ...
        """
        fake_trip = {'distance': 1000}
        fake_mode = {'base_mode': 'CAR', 'passengers': 1,
                     'footprint': {'gasoline': {'wh_per_km': 100}}}
        
        (footprint, metadata) = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)

        expected_footprint = {'kwh': 0.1, 'kg_co2': 0.1 * util.FUELS_KG_CO2_PER_KWH['gasoline']}
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

    def test_nyc_bus_footprint(self):
        """
        10 km in a NYC BUS should consume 16.90 kWh and emit 714.99 kg CO2e.
        """
        fake_trip = {
            'distance': 10000,
            'start_fmt_time': '2022-01-01',
            'start_loc': {'coordinates': [-74.006, 40.7128]}
        }
        fake_mode = {'base_mode': 'BUS'}

        (footprint, metadata) = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)

        expected_footprint = {'kwh': 16.90, 'kg_co2': 714.99}
        expected_metadata = {
            "data_sources": ["ntd2022", "egrid2022"],
            "is_provisional": False,
            "requested_year": 2022,
            "ntd_uace_code": "63217",
            "ntd_modes": ["MB", "RB", "CB"],
        }
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])
