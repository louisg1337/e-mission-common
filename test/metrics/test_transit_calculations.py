import unittest

import emcommon.metrics.footprint.transit_calculations as emcmft
import emcommon.diary.base_modes as emcdb
from emcommon.metrics.footprint.ntd_data_by_year import ntd_data

NYC_UACE_CODE = "63217"
CHICAGO_UACE_CODE = "16264"

BUS_MODES = emcdb.BASE_MODES['BUS']['footprint']['transit']
TRAIN_MODES = emcdb.BASE_MODES['TRAIN']['footprint']['transit']


class TestTransitCalculations(unittest.TestCase):
    def test_get_uace_by_zipcode(self):
        # https://www.cincinnati-oh.gov/finance/income-taxes/resources-references/street-listings-guide/
        # "ZIP Codes Entirely Within Cincinnati"
        cincinnati_zip_codes = ["45220", "45221", "45201", "45202",
                                "45203", "45206", "45210", "45214",
                                "45219", "45220", "45221", "45223",
                                "45225", "45226", "45228", "45232",
                                "45234", "45250", "45267"]
        cincinnati_uace_code = "16885"
        for zipcode in cincinnati_zip_codes:
            print("Testing zipcode: ", zipcode)
            result = emcmft.get_uace_by_zipcode(zipcode, 2022)
            self.assertEqual(result, cincinnati_uace_code)

    def test_bus_nyc(self):
        [intensities, metadata] = emcmft.get_intensities(2022, NYC_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 663.16, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 24)

    def test_bus_chicago(self):
        [intensities, metadata] = emcmft.get_intensities(2022, CHICAGO_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 1072.50, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 3)

    def test_bus_nationwide(self):
        [intensities, metadata] = emcmft.get_intensities(2022, None, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 867.36, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 415)

    def test_train_nyc(self):
        [intensities, metadata] = emcmft.get_intensities(2022, NYC_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 164.68, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 6)

    def test_train_chicago(self):
        [intensities, metadata] = emcmft.get_intensities(2022, CHICAGO_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 401.71, places=2)
        # only 2 passenger rail lines in Chicago - "the L" and Metra !
        self.assertEqual(len(metadata['ntd_ids']), 2)

    def test_train_nationwide(self):
        [intensities, metadata] = emcmft.get_intensities(2022, None, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 240.85, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 40)

    def test_all_modes_nationwide(self):
        [intesities, metadata] = emcmft.get_intensities(2022, None, None)
        self.assertAlmostEqual(intesities['overall']['wh_per_km'], 547.53, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 487)


class TestTransitCalculationsFakeData(unittest.TestCase):
    def test_get_intensities_fake_data2(self):
        """
        Example scenario from:
        https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2263813540
        """
        ntd_data["2022"].extend([
            {"NTD ID": "Agency A", "UACE Code": "foo", "Mode": "MB",
                "Diesel (km)": 12000, "Diesel (Wh/km)": 3000, "All Fuels (km)": 12000,
                "Passenger km": 60000, "Vehicle km": 12000, "Average Passengers": 5},
            {"NTD ID": "Agency A", "UACE Code": "foo", "Mode": "RB",
                "Electric (km)": 3000, "Electric (Wh/km)": 2000, "All Fuels (km)": 3000,
                "Passenger km": 15000, "Vehicle km": 3750, "Average Passengers": 4},
            {"NTD ID": "Agency B", "UACE Code": "foo", "Mode": "MB",
                "Diesel (km)": 3200, "Diesel (Wh/km)": 2000,
                "Electric (km)": 800, "Electric (Wh/km)": 1500, "All Fuels (km)": 4000,
                "Passenger km": 25000, "Vehicle km": 5000, "Average Passengers": 5},
        ])
        [intensities, metadata] = emcmft.get_intensities(2022, 'foo', BUS_MODES)
        self.assertDictEqual(intensities, {
            "diesel": {"wh_per_km": 550, "weight": 0.8},
            "electric": {"wh_per_km": 450, "weight": 0.2},
            "overall": {"wh_per_km": 530, "weight": 1.0},
        })
        self.assertDictEqual(metadata, {
            "source": "NTD",
            "is_provisional": False,
            "year": 2022,
            "requested_year": 2022,
            "uace_code": "foo",
            "modes": BUS_MODES,
            "ntd_ids": ["Agency A", "Agency B"],
        })
