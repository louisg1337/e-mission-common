// Transcrypt'ed from Python, 2024-08-06 23:57:25
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as util from './emcommon.metrics.footprint.util.js';
import * as transit from './emcommon.metrics.footprint.transit_calculations.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import {egrid_data} from './emcommon.metrics.footprint.egrid_carbon_by_year.js';
import * as Logger from './emcommon.logger.js';
export {egrid_data, emcdb, transit, Logger, util};
var __name__ = 'emcommon.metrics.footprint.footprint_calculations';
export var get_egrid_carbon_intensity = function (year, zipcode) {
	var metadata = {'source': 'eGRID', 'is_provisional': false, 'year': year, 'requested_year': year, 'zipcode': zipcode, 'egrid_region': null};
	if (!__in__ (str (year), egrid_data)) {
		var year = util.find_closest_available_year (year, egrid_data.py_keys ());
		metadata ['year'] = year;
		metadata ['is_provisional'] = true;
		Logger.log_warn ('eGRID data not available for year {}; '.format (metadata ['requested_year']) + 'Using closest available year {}'.format (metadata ['year']));
	}
	var egrid_data_for_year = egrid_data [str (year)];
	for (var r in egrid_data_for_year ['regions_zips']) {
		if (__in__ (zipcode, egrid_data_for_year ['regions_zips'] [r])) {
			metadata ['egrid_region'] = r;
			break;
		}
	}
	if (metadata ['egrid_region'] === null) {
		Logger.log_error ('eGRID region not found for zipcode {} in year {}'.format (zipcode, year));
		return null;
	}
	var kg_per_kwh = egrid_data_for_year ['regions_src2erta'] [metadata ['egrid_region']];
	return tuple ([kg_per_kwh, metadata]);
};
export var calc_footprint_for_trip = function (trip, mode_label_option) {
	Logger.log_debug ((('Getting footprint for trip: ' + str (trip)) + ', with mode option: ') + str (mode_label_option));
	var metadata = dict ({});
	var distance = trip ['distance'];
	var rich_mode = emcdb.get_rich_mode (mode_label_option);
	var mode_footprint = dict (rich_mode ['footprint']);
	if (__in__ ('transit', mode_footprint)) {
		var __left0__ = transit.get_intensities_for_trip (trip, mode_footprint ['transit']);
		var mode_footprint = __left0__ [0];
		var metadata = __left0__ [1];
	}
	var kwh_total = 0;
	var kg_co2_total = 0;
	for (var [fuel_type, fuel_type_footprint] of mode_footprint.py_items ()) {
		var kwh = ((distance / 1000) * fuel_type_footprint ['wh_per_km']) / 1000;
		if (__in__ (fuel_type, util.FUELS_KG_CO2_PER_KWH)) {
			Logger.log_debug ('Using default carbon intensity for fuel type: ' + fuel_type);
			var kg_co2 = kwh * util.FUELS_KG_CO2_PER_KWH [fuel_type];
		}
		else if (fuel_type == 'electric') {
			Logger.log_debug ('Using eGRID carbon intensity for electric');
			var year = util.year_of_trip (trip);
			var zipcode = trip ['start_confirmed_place'] ['zipcode'];
			var __left0__ = get_egrid_carbon_intensity (year, zipcode);
			var kg_per_kwh = __left0__ [0];
			var metadata = __left0__ [1];
			var kg_co2 = kwh * kg_per_kwh;
		}
		else {
			Logger.log_warn ('Unknown fuel type: ' + fuel_type);
			continue;
		}
		kwh_total += kwh;
		kg_co2_total += kg_co2;
	}
	var passengers = (__in__ ('passengers', mode_label_option) ? mode_label_option ['passengers'] : 1);
	return dict ({'kwh': kwh_total / passengers, 'kg_co2': kg_co2_total / passengers, 'metadata': metadata});
};

//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.map