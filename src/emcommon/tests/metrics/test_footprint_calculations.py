import unittest

import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import emcommon.metrics.footprint.util as util

KG_PER_LB = 0.453592


class TestTransitCalculations(unittest.TestCase):
    def test_get_egrid_carbon_intensity(self):
        # expected values (collected from https://www.epa.gov/egrid/data-explorer)
        # "I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
        # at the <eGRID subregion> level for <2022>."
        expected_lbs_per_kwh = {
            'RFCW': 1005.90,
            'NWPP': 605.87,
        }

        # Cincinnati, OH (RFCW region)
        [kg_per_kwh, metadata] = footprint_calculations.get_egrid_carbon_intensity(2022, "45221")
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
            "zipcode": "45221",
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

    def test_nyc_transit_footprint(self):
        fake_trip = {
            'distance': 10000,
            'start_fmt_time': '2022-01-01',
            'start_confirmed_place': {'zipcode': '10001'},
        }
        fake_mode = {'base_mode': 'BUS'}
        expected_footprint = {'kwh': 22.65, 'kg_co2': 1098.96}
        footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode)
        for key in expected_footprint:
            self.assertAlmostEqual(footprint[key], expected_footprint[key], places=2)

        fake_mode = {'base_mode': 'TRAIN'}
        expected_footprint = {'kwh': 22.65, 'kg_co2': 1098.96}
