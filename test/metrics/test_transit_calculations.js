import { footprint_calculations, base_modes, obj_to_dict } from '../../emcommon_js/index.js';
import { dict } from '../../emcommon_js/org.transcrypt.__runtime__.js';

const transit_calculations = footprint_calculations.transit;
const ntd_data = footprint_calculations.transit.ntd_data;

const NYC_UACE_CODE = '63217';
const CHICAGO_UACE_CODE = '16264';

const BUS_MODES = base_modes.BASE_MODES['BUS']['footprint']['transit'];
const TRAIN_MODES = base_modes.BASE_MODES['TRAIN']['footprint']['transit'];

describe('TestTransitCalculations', () => {
  it('test_get_uace_by_zipcode', () => {
    // https://www.cincinnati-oh.gov/finance/income-taxes/resources-references/street-listings-guide/
    // "ZIP Codes Entirely Within Cincinnati"
    const cincinnati_zip_codes = [
      '45220',
      '45221',
      '45201',
      '45202',
      '45203',
      '45206',
      '45210',
      '45214',
      '45219',
      '45220',
      '45221',
      '45223',
      '45225',
      '45226',
      '45228',
      '45232',
      '45234',
      '45250',
      '45267',
    ];
    const cincinnati_uace_code = '16885';
    for (const zipcode of cincinnati_zip_codes) {
      console.debug('Testing zipcode: ', zipcode);
      const result = transit_calculations.get_uace_by_zipcode(zipcode, 2022);
      expect(result).toEqual(cincinnati_uace_code);
    }
  });

  it('test_bus_nyc', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      NYC_UACE_CODE,
      BUS_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(663.16, 2);
    expect(metadata['ntd_ids'].length).toEqual(24);
  });

  it('test_bus_chicago', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      CHICAGO_UACE_CODE,
      BUS_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(1072.5, 2);
    expect(metadata['ntd_ids'].length).toEqual(3);
  });

  it('test_bus_nationwide', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      null,
      BUS_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(867.36, 2);
    expect(metadata['ntd_ids'].length).toEqual(415);
  });

  it('test_train_nyc', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      NYC_UACE_CODE,
      TRAIN_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(164.68, 2);
    expect(metadata['ntd_ids'].length).toEqual(6);
  });

  it('test_train_chicago', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      CHICAGO_UACE_CODE,
      TRAIN_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(401.71, 2);
    // only 2 passenger rail lines in Chicago - "the L" and Metra !
    expect(metadata['ntd_ids'].length).toEqual(2);
  });

  it('test_train_nationwide', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      null,
      TRAIN_MODES,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(240.85, 2);
    expect(metadata['ntd_ids'].length).toEqual(40);
  });

  it('test_all_modes_nationwide', () => {
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      null,
      null,
    );
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(547.53, 2);
    expect(metadata['ntd_ids'].length).toEqual(487);
  });
});

describe('TestTransitCalculationsFakeData', () => {
  it('test_get_intensities_fake_data2', () => {
    /**
     * Example scenario from:
     * https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2263813540
     */
    ntd_data['2022'].push(
      dict({
        'NTD ID': 'Agency A',
        'UACE Code': 'foo',
        Mode: 'MB',
        'Diesel (km)': 12000,
        'Diesel (Wh/km)': 3000,
        'All Fuels (km)': 12000,
        'Passenger km': 60000,
        'Vehicle km': 12000,
        'Average Passengers': 5,
      }),
    );
    ntd_data['2022'].push(
      dict({
        'NTD ID': 'Agency A',
        'UACE Code': 'foo',
        Mode: 'RB',
        'Electric (km)': 3000,
        'Electric (Wh/km)': 2000,
        'All Fuels (km)': 3000,
        'Passenger km': 15000,
        'Vehicle km': 3750,
        'Average Passengers': 4,
      }),
    );
    ntd_data['2022'].push(
      dict({
        'NTD ID': 'Agency B',
        'UACE Code': 'foo',
        Mode: 'MB',
        'Diesel (km)': 3200,
        'Diesel (Wh/km)': 2000,
        'Electric (km)': 800,
        'Electric (Wh/km)': 1500,
        'All Fuels (km)': 4000,
        'Passenger km': 25000,
        'Vehicle km': 5000,
        'Average Passengers': 5,
      }),
    );
    const [intensities, metadata] = transit_calculations.get_intensities_for_year_and_uace(
      2022,
      'foo',
      BUS_MODES,
    );
    console.debug({ intensities });
    expect(intensities).toEqual({
      diesel: { wh_per_km: 550, weight: 0.8 },
      electric: { wh_per_km: 450, weight: 0.2 },
      overall: { wh_per_km: 530, weight: 1.0 },
    });
    expect(metadata).toEqual({
      source: 'NTD',
      is_provisional: false,
      year: 2022,
      requested_year: 2022,
      uace_code: 'foo',
      modes: BUS_MODES,
      ntd_ids: ['Agency A', 'Agency B'],
    });
  });
});
