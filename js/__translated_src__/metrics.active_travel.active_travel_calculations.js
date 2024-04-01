// Transcrypt'ed from Python, 2024-04-01 15:20:09
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {standard_met_mode_map} from './metrics.active_travel.standard_met_mode_map.js';
import {log_warn} from './logger.js';
var __name__ = 'metrics.active_travel.active_travel_calculations';
export var get_mets_mode_map = function (label_options) {
	var mode_options = label_options ['MODE'];
	var mode_met_entries = [];
	for (var opt of mode_options) {
		if (opt.py_get ('met_equivalent')) {
			var curr_met = standard_met_mode_map [opt ['met_equivalent']];
			mode_met_entries.append ([opt ['value'], curr_met]);
		}
		else if (opt.py_get ('met')) {
			var curr_met = opt ['met'];
			for (var range_name of curr_met) {
				curr_met [range_name] ['range'] = (function () {
					var __accu0__ = [];
					for (var i of curr_met [range_name] ['range']) {
						__accu0__.append ((i != -(1) ? i : float ('inf')));
					}
					return __accu0__;
				}) ();
			}
			mode_met_entries.append ([opt ['value'], curr_met]);
		}
		else {
			log_warn ('Did not find either met_equivalent or met for {} ignoring entry'.format (opt ['value']));
		}
	}
	return mode_met_entries;
};

//# sourceMappingURL=metrics.active_travel.active_travel_calculations.map