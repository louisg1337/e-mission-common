// Transcrypt'ed from Python, 2024-03-13 01:21:52
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {log_debug} from './logger.js';
var __name__ = 'metrics.carbon.carbon_calculations';
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
	var mode_co2_entries = [];
	var range_limited_motorized = null;
	for (var opt of mode_options) {
		if (opt.py_get ('range_limit_km')) {
			if (range_limited_motorized) {
				log_debug ('Found two range limited motorized options: {} and {}'.format (range_limited_motorized, opt));
			}
			var range_limited_motorized = opt;
			log_debug ('Found range limited motorized mode - {}'.format (range_limited_motorized));
		}
		if (opt.py_get ('kgCo2PerKm') !== null) {
			mode_co2_entries.append ([opt ['value'], opt ['kgCo2PerKm']]);
		}
	}
	return mode_co2_entries;
};

//# sourceMappingURL=metrics.carbon.carbon_calculations.map