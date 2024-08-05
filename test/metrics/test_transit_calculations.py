import unittest

import emcommon.metrics.footprint.transit_calculations as emcmft
import emcommon.diary.base_modes as emcdb
from emcommon.metrics.footprint.ntd_data_by_year import ntd_data
from .test_footprint_calculations import CINCINNATI_ZIP_CODES

NYC_UACE_CODE = "63217"
CHICAGO_UACE_CODE = "16264"

BUS_MODES = emcdb.BASE_MODES['BUS']['footprint']['transit']
TRAIN_MODES = emcdb.BASE_MODES['TRAIN']['footprint']['transit']


class TestTransitCalculations(unittest.TestCase):
    def test_get_uace_by_zipcode(self):
        cincinnati_uace_code = "16885"
        for zipcode in CINCINNATI_ZIP_CODES:
            print("Testing zipcode: ", zipcode)
            result = emcmft.get_uace_by_zipcode(zipcode, 2022)
            self.assertEqual(result, cincinnati_uace_code)

    def test_bus_nyc(self):
        [intensities, metadata] = emcmft.get_intensities(2022, NYC_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 646.80, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 22)

    def test_bus_chicago(self):
        [intensities, metadata] = emcmft.get_intensities(2022, CHICAGO_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 1048.12, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 2)

    def test_bus_nationwide(self):
        [intensities, metadata] = emcmft.get_intensities(2022, None, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 809.03, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 405)

    def test_train_nyc(self):
        [intensities, metadata] = emcmft.get_intensities(2022, NYC_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 24.79, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 6)

    def test_train_chicago(self):
        [intensities, metadata] = emcmft.get_intensities(2022, CHICAGO_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 159.04, places=2)
        # 3 passenger rail systems in Chicago - "the L", Metra, and South Shore Line
        self.assertEqual(len(metadata['ntd_ids']), 3)

    def test_train_nationwide(self):
        [intensities, metadata] = emcmft.get_intensities(2022, None, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 67.71, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 48)

    def test_all_modes_nationwide(self):
        [intesities, metadata] = emcmft.get_intensities(2022, None, None)
        self.assertAlmostEqual(intesities['overall']['wh_per_km'], 485.08, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 517)


class TestTransitCalculationsFakeData(unittest.TestCase):
    def test_get_intensities_fake_data2(self):
        """
        Example scenario from:
        https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2263813540
        """
        ntd_data["2022"].extend([
            {"NTD ID": "Agency A", "UACE Code": "foo", "Mode": "MB",
             "Diesel (Wh/pkm)": 600, "Diesel (%)": 100,
             "Unlinked Passenger Trips": 600},
            {"NTD ID": "Agency A", "UACE Code": "foo", "Mode": "RB",
             "Electric (Wh/pkm)": 500, "Electric (%)": 100,
             "Unlinked Passenger Trips": 150},
            {"NTD ID": "Agency B", "UACE Code": "foo", "Mode": "MB",
             "Diesel (Wh/pkm)": 400, "Diesel (%)": 80,
             "Electric (Wh/pkm)": 300, "Electric (%)": 20,
             "Unlinked Passenger Trips": 250}
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
