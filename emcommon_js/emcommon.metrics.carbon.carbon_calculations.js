// Transcrypt'ed from Python, 2024-04-16 22:35:59
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as Logger from './emcommon.logger.js';
export {Logger};
var __name__ = 'emcommon.metrics.carbon.carbon_calculations';
export var km_per_mile = 1.609344;
export var kwh_per_gallon = 33.7;
export var default_car_footprint = 278 / 1609;
export var default_mpg = 8.91 / (1.6093 * default_car_footprint);
export var mpg_to_co2_per_km = (function __lambda__ (mpg) {
	return (1 / (mpg * km_per_mile)) * 8.91;
});
export var default_carbon_mode_map = dict ({'walking': 0, 'running': 0, 'cycling': 0, 'mixed': 0, 'bus_short': 267.0 / 1609, 'bus_long': 267.0 / 1609, 'train_short': 92.0 / 1609, 'train_long': 92.0 / 1609, 'car_short': mpg_to_co2_per_km (default_mpg), 'car_long': mpg_to_co2_per_km (default_mpg), 'air_short': 217.0 / 1609, 'air_long': 217.0 / 1609});
export var get_carbon_mode_map = function (label_options) {
	var mode_options = label_options ['MODE'];
	var mode_co2_entries = dict ({});
	var range_limited_motorized = null;
	for (var opt of mode_options) {
		if (__in__ ('range_limit_km', opt)) {
			if (range_limited_motorized) {
				Logger.log_debug ('Found two range limited motorized options: {} and {}'.format (range_limited_motorized, opt));
			}
			var range_limited_motorized = opt;
			Logger.log_debug ('Found range limited motorized mode - {}'.format (range_limited_motorized));
		}
		if (__in__ ('kgCo2PerKm', opt)) {
			mode_co2_entries [opt ['value']] = opt ['kgCo2PerKm'];
		}
	}
	return mode_co2_entries;
};
export var highest_carbon_mode = function (label_options) {
	var mode_co2_entries = get_carbon_mode_map (label_options);
	return max (mode_co2_entries, __kwargtrans__ ({key: mode_co2_entries.py_get}));
};
export var carbon_summary_by_mode = function (composite_trips, label_options) {
	var mode_to_distance_map = distance_summary_by_mode (composite_trips);
	var mode_to_carbon_map = get_carbon_mode_map (label_options);
	var carbon_summary = dict ({});
	for (var [mode, distance] of mode_to_distance_map.py_items ()) {
		carbon_summary [mode] = distance * mode_to_carbon_map [mode];
	}
	return carbon_summary;
};

//# sourceMappingURL=emcommon.metrics.carbon.carbon_calculations.map