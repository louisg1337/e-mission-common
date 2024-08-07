export const fuel_types: string[];
export function weighted_mean(py_values: any, weights: any): number;
export function get_uace_by_zipcode(zipcode: any, year: any): any;
export function get_intensities_for_trip(trip: any, modes: any): any;
export function get_intensities(year: any, uace: any, modes: any): any;
import * as Logger from './emcommon.logger.js';
import { ntd_data } from './emcommon.metrics.footprint.ntd_data_by_year.js';
import * as util from './emcommon.metrics.footprint.util.js';
import { uace_zip_maps } from './emcommon.metrics.footprint.ntd_data_by_year.js';
export { Logger, ntd_data, util, uace_zip_maps };
//# sourceMappingURL=emcommon.metrics.footprint.transit_calculations.d.ts.map