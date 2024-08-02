import { footprint_calculations } from "../../emcommon_js/index";

const KG_PER_LB = 0.453592;
const FUELS_KG_CO2_PER_KWH = footprint_calculations.util.FUELS_KG_CO2_PER_KWH;

describe('TestFootprintCalculations', () => {
  it('test_get_egrid_carbon_intensity', () => {
    /* expected values (collected from https://www.epa.gov/egrid/data-explorer)
    "I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
    at the <eGRID subregion> level for <2022>."
    */
    const expected_lbs_per_kwh = {
      'RFCW': 1005.90,
      'NWPP': 605.87,
    };

    // Cincinnati, OH (RFCW region)
    const [kg_per_kwh, metadata] = footprint_calculations.get_egrid_carbon_intensity(2022, '45221');
    expect(kg_per_kwh).toBeCloseTo(expected_lbs_per_kwh['RFCW'] * KG_PER_LB, 2);
    expect(metadata).toEqual({
      'source': 'eGRID',
      'is_provisional': false,
      'year': 2022,
      'requested_year': 2022,
      'zipcode': '45221',
      'egrid_region': 'RFCW',
    });

    // Eagle Point, OR (NWPP region)
    const [kg_per_kwh2, metadata2] = footprint_calculations.get_egrid_carbon_intensity(2023, '97524');
    expect(kg_per_kwh2).toBeCloseTo(expected_lbs_per_kwh['NWPP'] * KG_PER_LB, 2);
    expect(metadata2).toEqual({
      'source': 'eGRID',
      'is_provisional': true,
      'year': 2022,
      'requested_year': 2023,
      'zipcode': '97524',
      'egrid_region': 'NWPP',
    });
  });
  it('test_car_default_footprint', () => {
    // 1 km in a default CAR should consume 0.87 kWh and emit 0.23 kg CO2e.
    const fake_trip = { distance: 1000 };
    const fake_mode = { base_mode: 'CAR', passengers: 1 };
    const footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode);
    expect(footprint).toMatchObject({
      kwh: expect.closeTo(0.87),
      kg_co2: expect.closeTo(0.23),
    });

    // with 2 passengers, the footprint should be halved
    fake_mode.passengers = 2;
    const footprint2 = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode);
    expect(footprint2).toMatchObject({
      kwh: expect.closeTo(0.87 / 2),
      kg_co2: expect.closeTo(0.23 / 2),
    });
  });

  it('test_car_custom_footprint', () => {
    // 1 km in a custom CAR (wh/km = 100) should consume 0.1 kWh and ...
    const fake_trip = { distance: 1000 };
    const fake_mode = {
      base_mode: 'CAR',
      passengers: 1,
      footprint: { gasoline: { wh_per_km: 100 } },
    };
    const footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode);
    expect(footprint).toMatchObject({
      kwh: expect.closeTo(0.1),
      kg_co2: expect.closeTo(0.1 * FUELS_KG_CO2_PER_KWH['gasoline']),
    });
  });

  it('test_nyc_transit_footprint', () => {
    const fake_trip = {
      distance: 10000,
      start_fmt_time: '2022-01-01',
      start_confirmed_place: { zipcode: '10001' },
    };
    const fake_mode = { base_mode: 'BUS' };
    const footprint = footprint_calculations.calc_footprint_for_trip(fake_trip, fake_mode);
    expect(footprint).toMatchObject({
      kwh: expect.closeTo(22.65),
      kg_co2: expect.closeTo(1098.96),
    });
  });
});
