export function get_egrid_carbon_intensity(year: any, coords: any): Promise<any>;
export function merge_metadatas(meta_a: any, meta_b: any): void;
export function calc_footprint_for_trip(trip: any, mode_label_option: any): Promise<any>;
import * as util from './emcommon.metrics.footprint.util.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Logger from './emcommon.logger.js';
import * as emcutil from './emcommon.util.js';
import * as transit from './emcommon.metrics.footprint.transit_calculations.js';
export { util, emcdb, Logger, emcutil, transit };
//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.d.ts.map