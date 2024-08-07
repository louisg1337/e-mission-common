export const KWH_PER_GALLON_GASOLINE: number;
export const DIESEL_GGE: number;
export const FUELS_KG_CO2_PER_KWH: {};
export const MI_PER_KM: number;
export function mpge_to_wh_per_km(mpge: any): number;
export function get_egrid_carbon_intensity(year: any, zipcode: any): any;
export function calc_footprint_for_trip(trip: any, mode_label_option: any): {};
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Logger from './emcommon.logger.js';
import { egrid_data } from './emcommon.metrics.footprint.egrid_carbon_by_year.js';
export { emcdb, Logger, egrid_data };
//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.d.ts.map