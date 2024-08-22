import * as emcmff from "../../emcommon_js/emcommon.metrics.footprint.footprint_calculations";
import * as emcmfu from "../../emcommon_js/emcommon.metrics.footprint.util";


const KG_PER_LB = 0.453592;

/*
eGRID expected values (collected from https://www.epa.gov/egrid/data-explorer)
"I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
at the <eGRID subregion> level for <2022>."
*/
const EGRID_EXPECTED_LBS_PER_KWH = {
  'RFCW': 1005.90,
  'NWPP': 605.87,
};


describe('TestFootprintCalculations', () => {
  it('test_get_egrid_intensity_cincinnati_2022', async () => {
    const coords = [-84.52, 39.13];
    const [kg_per_kwh, metadata] = await emcmff.get_egrid_intensity_for_coords(2022, coords);

    const expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["RFCW"] * KG_PER_LB;
    const expected_metadata = {
      "data_sources": ["egrid2022"],
      "data_source_urls": [
        "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
      ],
      "is_provisional": false,
      "requested_year": 2022,
      "requested_coords": coords,
      "egrid_region": "RFCW",
    };
    expect(kg_per_kwh).toBeCloseTo(expected_kg_per_kwh, 2);
    expect(metadata).toEqual(expected_metadata);
  });

  it('test_get_egrid_intensity_eagle_point_2023', async () => {
    const coords = [-122.83, 42.29];
    const [kg_per_kwh, metadata] = await emcmff.get_egrid_intensity_for_coords(2023, coords);

    const expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["NWPP"] * KG_PER_LB;
    const expected_metadata = {
      "data_sources": ["egrid2022"],
      "data_source_urls": [
        "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
      ],
      "is_provisional": true,
      "requested_year": 2023,
      "requested_coords": coords,
      "egrid_region": "NWPP",
    };
    expect(kg_per_kwh).toBeCloseTo(expected_kg_per_kwh, 2);
    expect(metadata).toEqual(expected_metadata);
  });

  it('test_car_default_footprint', async () => {
    const fake_trip = {'distance': 1000};
    const fake_mode = {'base_mode': 'CAR', 'passengers': 1};

    const [footprint, metadata] = await emcmff.calc_footprint_for_trip(fake_trip, fake_mode);

    const expected_footprint = {'kwh': 0.87, 'kg_co2': 0.23};
    for (const key in expected_footprint) {
      expect(footprint[key]).toBeCloseTo(expected_footprint[key], 2);
    }

    // with 2 passengers, the footprint should be halved
    fake_mode['passengers'] = 2;

    const [footprint2, metadata2] = await emcmff.calc_footprint_for_trip(fake_trip, fake_mode);

    const expected_footprint2 = {'kwh': 0.87 / 2, 'kg_co2': 0.23 / 2};
    for (const key in expected_footprint2) {
      expect(footprint2[key]).toBeCloseTo(expected_footprint2[key], 2);
    }
  });

  it('test_car_custom_footprint', async () => {
    const fake_trip = {'distance': 1000};
    const fake_mode = {'base_mode': 'CAR', 'passengers': 1,
                     'footprint': {'gasoline': {'wh_per_km': 100}}};
    
    const [footprint, metadata] = await emcmff.calc_footprint_for_trip(fake_trip, fake_mode);

    const expected_footprint = {'kwh': 0.1, 'kg_co2': 0.1 * emcmfu.FUELS_KG_CO2_PER_KWH['gasoline']};
    for (const key in expected_footprint) {
      expect(footprint[key]).toBeCloseTo(expected_footprint[key], 2);
    }
  });

  it('test_nyc_bus_footprint', async () => {
    const fake_trip = {
      'distance': 10000,
      'start_fmt_time': '2022-01-01',
      'start_loc': {'coordinates': [-74.006, 40.7128]}
    };
    const fake_mode = {'base_mode': 'BUS'};

    const [footprint, metadata] = await emcmff.calc_footprint_for_trip(fake_trip, fake_mode);

    const expected_footprint = {'kwh': 16.90, 'kg_co2': 714.99};
    const expected_metadata = {
      "data_sources": ["ntd2022", "egrid2022"],
      "is_provisional": false,
      "requested_year": 2022,
      "ntd_uace_code": "63217",
      "ntd_modes": ["MB", "RB", "CB"],
    };
    for (const key in expected_footprint) {
      expect(footprint[key]).toBeCloseTo(expected_footprint[key], 2);
    }
    for (const key in expected_metadata) {
      expect(metadata[key]).toEqual(expected_metadata[key]);
    }
  });
});
