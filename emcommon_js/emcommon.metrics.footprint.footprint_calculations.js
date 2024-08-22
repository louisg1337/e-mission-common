// Transcrypt'ed from Python, 2024-08-22 03:48:37
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as util from './emcommon.metrics.footprint.util.js';
import * as transit from './emcommon.metrics.footprint.transit_calculations.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as emcutil from './emcommon.util.js';
import * as Logger from './emcommon.logger.js';
export {util, emcdb, Logger, emcutil, transit};
var __name__ = 'emcommon.metrics.footprint.footprint_calculations';
export var get_egrid_carbon_intensity = async function (year, coords) {
	if (typeof coords == 'undefined' || (coords != null && coords.hasOwnProperty ("__kwargtrans__"))) {;
		var coords = null;
	};
	Logger.log_debug ('Getting eGRID carbon intensity for year {} and coords {}'.format (year, coords));
	var intensities_data = await util.get_intensities_data (year, 'egrid');
	var actual_year = intensities_data ['metadata'] ['year'];
	var metadata = {'data_sources': ['egrid{}'.format (actual_year)], 'data_source_urls': intensities_data ['metadata'] ['data_source_urls'], 'is_provisional': actual_year != year, 'requested_year': year, 'egrid_coords': coords, 'egrid_region': null};
	if (coords !== null) {
		metadata ['egrid_region'] = await util.get_egrid_region (coords, actual_year);
	}
	if (metadata ['egrid_region'] === null) {
		if (coords !== null) {
			Logger.log_warn ('eGRID region not found for coords {} in year {}. Using national average.'.format (coords, year));
		}
		else {
			Logger.log_debug ('Coords not given for eGRID lookup in year {}. Using national average.'.format (year));
		}
		var kg_per_kwh = intensities_data ['national_kg_per_mwh'];
		return null;
	}
	else {
		var kg_per_kwh = intensities_data ['regions_kg_per_mwh'] [metadata ['egrid_region']];
	}
	return tuple ([kg_per_kwh, metadata]);
};
export var merge_metadatas = function (meta_a, meta_b) {
	for (var key in meta_b) {
		var value = meta_b [key];
		if (!__in__ (key, meta_a)) {
			meta_a [key] = value;
		}
		else if (hasattr (meta_a [key], 'concat')) {
			meta_a [key] = meta_a [key].concat (value);
		}
		else if (isinstance (value, list)) {
			meta_a [key] = meta_a [key] + value;
		}
		else if (isinstance (value, bool)) {
			meta_a [key] = meta_a [key] || value;
		}
		else {
			meta_a [key] = value;
		}
	}
};
export var calc_footprint_for_trip = async function (trip, mode_label_option) {
	Logger.log_debug ((('Getting footprint for trip: ' + str (trip)) + ', with mode option: ') + str (mode_label_option));
	var metadata = dict ({});
	var distance = trip ['distance'];
	var rich_mode = emcdb.get_rich_mode (mode_label_option);
	var mode_footprint = dict (rich_mode ['footprint']);
	if (__in__ ('transit', mode_footprint)) {
		var __left0__ = await transit.get_intensities_for_trip (trip, mode_footprint ['transit']);
		var mode_footprint = __left0__ [0];
		var transit_metadata = __left0__ [1];
		merge_metadatas (metadata, transit_metadata);
	}
	var kwh_total = 0;
	var kg_co2_total = 0;
	for (var fuel_type in mode_footprint) {
		var fuel_type_footprint = mode_footprint [fuel_type];
		var kwh = ((distance / 1000) * fuel_type_footprint ['wh_per_km']) / 1000;
		if (__in__ (fuel_type, util.FUELS_KG_CO2_PER_KWH)) {
			Logger.log_debug ('Using default carbon intensity for fuel type: ' + fuel_type);
			var kg_co2 = kwh * util.FUELS_KG_CO2_PER_KWH [fuel_type];
		}
		else if (fuel_type == 'electric') {
			Logger.log_debug ('Using eGRID carbon intensity for electric');
			var year = util.year_of_trip (trip);
			var coords = trip ['start_loc'] ['coordinates'];
			var __left0__ = await get_egrid_carbon_intensity (year, coords);
			var kg_per_kwh = __left0__ [0];
			var egrid_metadata = __left0__ [1];
			merge_metadatas (metadata, egrid_metadata);
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
	var footprint = dict ({'kwh': kwh_total / passengers, 'kg_co2': kg_co2_total / passengers});
	return tuple ([footprint, metadata]);
};

//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.map