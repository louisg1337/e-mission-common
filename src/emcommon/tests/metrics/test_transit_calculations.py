import unittest

import emcommon.metrics.footprint.transit_calculations as emcmft
from emcommon.metrics.footprint.ntd_data_by_year import ntd_data


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

    def test_get_intensities_nyc(self):
        nyc_uace_code = "63217"

        [intensities, _] = emcmft.get_intensities_for_year_and_uace(2022,
                                                                    nyc_uace_code,
                                                                    ["MB", "RB", "CB"])
        self.assertDictEqual(intensities, {
            'gasoline': {'wh_per_km': 1150.6149060903217, 'weight': 0.0006802051357443231},
            'diesel': {'wh_per_km': 704.4978022926837, 'weight': 0.9257180207917586},
            'cng': {'wh_per_km': 137.66763797167093, 'weight': 0.07299997705641229},
            'electric': {'wh_per_km': 271.9668109308468, 'weight': 0.0006017970160848553},
            'overall': {'wh_per_km': 663.1623685875481, 'weight': 1.0}
        })

        # train
        [intensities, _] = emcmft.get_intensities_for_year_and_uace(2022,
                                                                    nyc_uace_code,
                                                                    ["LR", "YR", "HR"])
        print(intensities)
        self.assertDictEqual(intensities, {
            'diesel': {'wh_per_km': 622.4276439477787, 'weight': 0.003411661772594213},
            'electric': {'wh_per_km': 140.73811153245256, 'weight': 0.9965883382274059},
            'overall': {'wh_per_km': 142.38147329645273, 'weight': 1.0}
        })

    def test_get_intensities_chicago(self):
        chicago_uace_code = "16264"

        # bus
        [intensities, _] = emcmft.get_intensities_for_year_and_uace(2022,
                                                                    chicago_uace_code,
                                                                    ["MB", "RB"])
        self.assertDictEqual(intensities, {
            'cng': {'wh_per_km': 414.17270183774167, 'weight': 0.035940657379679074},
            'diesel': {'wh_per_km': 1098.7288094019307, 'weight': 0.962139160550334},
            'electric': {'wh_per_km': 251.77739332732477, 'weight': 0.0019201820699868985},
            'overall': {'wh_per_km': 1072.4991119595031, 'weight': 0.9999999999999999},
        })

        # train
        [intensities, _] = emcmft.get_intensities_for_year_and_uace(2022,
                                                                    chicago_uace_code,
                                                                    ["LR", "YR", "HR"])
        self.assertDictEqual(intensities, {
            'electric': {'wh_per_km': 418.97212132658365, 'weight': 1.0},
            'overall': {'wh_per_km': 418.97212132658365, 'weight': 1.0},
        })

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
        [intensities, _] = emcmft.get_intensities_for_year_and_uace(2022,
                                                                    "foo",
                                                                    ["MB", "RB"])
        self.assertDictEqual(intensities, {
            "diesel": {"wh_per_km": 550, "weight": 0.8},
            "electric": {"wh_per_km": 450, "weight": 0.2},
            "overall": {"wh_per_km": 530, "weight": 1.0},
        })
