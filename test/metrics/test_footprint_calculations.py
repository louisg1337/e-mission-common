import unittest

import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import emcommon.metrics.footprint.util as util

KG_PER_LB = 0.453592

# https://www.cincinnati-oh.gov/finance/income-taxes/resources-references/street-listings-guide/
CINCINNATI_ZIP_CODES = [
    # "ZIP Codes Entirely Within Cincinnati"
    "45220", "45221", "45201", "45202", "45203", "45206", # "45210" (Doesn't seem to exist)
    "45214", "45219", "45220", "45221", "45223", "45225", "45226", # "45228" (Exists but is not in the ZIP - ZCTA mapping)
    "45232", "45234", "45250", "45267", 
    # "ZIP Codes Located Inside/Outside of Cincinnati"
    "45204", "45205", "45207", "45208",
    "45209", "45211", "45212", "45213",
    "45215", "45216", "45217", "45224",
    "45227", "45229", "45230", "45231",
    "45233", "45237", "45238", "45239",
    "45248",
    # "ZIP Codes Entirely Outside of Cincinnati"
    "45218", "45236", "45240", "45241", "45242", "45243", "45244", "45245",
    "45246", "45247", "45249", "45251", "45252", "45253", "45254", "45255",
]

class TestFootprintCalculations(unittest.TestCase):
    def test_get_egrid_carbon_intensity(self):
        # expected values (collected from https://www.epa.gov/egrid/data-explorer)
        # "I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
        # at the <eGRID subregion> level for <2022>."
        expected_lbs_per_kwh = {
            'RFCW': 1005.90,
            'NWPP': 605.87,
        }

        # Cincinnati, OH (RFCW region)
        for zipcode in CINCINNATI_ZIP_CODES:
            print("Testing zipcode: ", zipcode)
            [kg_per_kwh, metadata] = footprint_calculations.get_egrid_carbon_intensity(2022, zipcode)
            self.assertAlmostEqual(
                kg_per_kwh,
                expected_lbs_per_kwh["RFCW"] * KG_PER_LB,
                places=2
            )
            expected_metadata = {
                "source": "eGRID",
                "is_provisional": False,
                "year": 2022,
                "requested_year": 2022,
                "zipcode": zipcode,
                "egrid_region": "RFCW",
            }
            for key in expected_metadata:
                self.assertEqual(metadata[key], expected_metadata[key])

        # Eagle Point, OR (NWPP region)
        [kg_per_kwh, metadata] = footprint_calculations.get_egrid_carbon_intensity(2023, "97524")
        self.assertAlmostEqual(
            kg_per_kwh,
            expected_lbs_per_kwh["NWPP"] * KG_PER_LB,
            places=2
        )
        expected_metadata = {
            "source": "eGRID",
            "is_provisional": True,
            "year": 2022,
            "requested_year": 2023,
            "zipcode": "97524",
            "egrid_region": "NWPP",
        }
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])

    def test_car_default_footprint(self):
        """
        1 km in a default CAR should consume 0.87 kWh and emit 0.23 kg CO2e.
        """
        fake_trip = {'distance': 1000}
        fake_mode = {'base_mode': 'CAR', 'passengers': 1}
        expected_footprint = {'kwh': 0.87, 'kg_co2': 0.23}
        footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

        # with 2 passengers, the footprint should be halved
        fake_mode['passengers'] = 2
        expected_footprint = {'kwh': 0.87 / 2, 'kg_co2': 0.23 / 2}
        footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

    def test_car_custom_footprint(self):
        """
        1 km in a custom CAR (wh/km = 100) should consume 0.1 kWh and ...
        """
        fake_trip = {'distance': 1000}
        fake_mode = {'base_mode': 'CAR', 'passengers': 1,
                     'footprint': {'gasoline': {'wh_per_km': 100}}}
        expected_footprint = {'kwh': 0.1, 'kg_co2': 0.1 * util.FUELS_KG_CO2_PER_KWH['gasoline']}
        footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

    def test_nyc_bus_footprint(self):
        fake_trip = {
            'distance': 10000,
            'start_fmt_time': '2022-01-01',
            'start_confirmed_place': {'zipcode': '10001'},
        }
        fake_mode = {'base_mode': 'BUS'}
        expected_footprint = {'kwh': 16.90, 'kg_co2': 714.99}
        footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)
