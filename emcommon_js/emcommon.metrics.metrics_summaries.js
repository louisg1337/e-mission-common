// Transcrypt'ed from Python, 2024-04-16 22:35:59
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as Logger from './emcommon.logger.js';
export {Logger};
var __name__ = 'emcommon.metrics.metrics_summaries';
export var labeled_mode_for_trip = function (composite_trip, trip_labels_map) {
	var UNLABELED = 'unlabeled';
	if (!(composite_trip)) {
		return UNLABELED;
	}
	if (__in__ ('user_input', composite_trip) && __in__ ('mode_confirm', composite_trip ['user_input'])) {
		return composite_trip ['user_input'] ['mode_confirm'];
	}
	if (trip_labels_map && __in__ (composite_trip ['_id'] ['$oid'], trip_labels_map)) {
		if (__in__ ('MODE', trip_labels_map [composite_trip ['_id'] ['$oid']])) {
			return trip_labels_map [composite_trip ['_id'] ['$oid']] ['MODE'] ['data'] ['label'];
		}
	}
	return UNLABELED;
};
export var generate_summaries = function (metrics, composite_trips, trip_labels_map) {
	return (function () {
		var __accu0__ = [];
		for (var metric of metrics) {
			__accu0__.append ([metric, get_summary_for_metric (metric, composite_trips, trip_labels_map)]);
		}
		return dict (__accu0__);
	}) ();
};
export var value_of_metric_for_trip = function (metric, trip, trip_labels_map) {
	if (metric == 'distance') {
		return trip ['distance'];
	}
	else if (metric == 'count') {
		return 1;
	}
	else if (metric == 'duration') {
		return trip ['duration'];
	}
	return null;
};
export var get_summary_for_metric = function (metric, composite_trips, trip_labels_map) {
	var days_of_metrics_data = dict ({});
	for (var trip of composite_trips) {
		var date = trip ['start_fmt_time'].py_split ('T') [0];
		if (!__in__ (date, days_of_metrics_data)) {
			days_of_metrics_data [date] = [];
		}
		days_of_metrics_data [date].append (trip);
	}
	var days_summaries = [];
	for (var [date, trips] of days_of_metrics_data.py_items ()) {
		var summary_for_day = dict ({'date': date});
		summary_for_day.py_update (metric_summary_by_mode (metric, trips, trip_labels_map));
		days_summaries.append (summary_for_day);
	}
	return days_summaries;
};
export var metric_summary_by_mode = function (metric, composite_trips, trip_labels_map) {
	var mode_to_metric_map = dict ({});
	if (!(composite_trips)) {
		return mode_to_metric_map;
	}
	for (var trip of composite_trips) {
		var mode_key = 'mode_' + labeled_mode_for_trip (trip, trip_labels_map);
		if (!__in__ (mode_key, mode_to_metric_map)) {
			mode_to_metric_map [mode_key] = 0;
		}
		mode_to_metric_map [mode_key] += value_of_metric_for_trip (metric, trip, trip_labels_map);
	}
	return mode_to_metric_map;
};

//# sourceMappingURL=emcommon.metrics.metrics_summaries.map