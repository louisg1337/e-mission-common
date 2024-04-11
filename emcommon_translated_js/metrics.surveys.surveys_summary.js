// Transcrypt'ed from Python, 2024-04-11 11:59:22
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {survey_prompted_for_trip} from './survey.conditional_surveys.js';
import * as Logger from './logger.js';
var __name__ = 'metrics.surveys.surveys_summary';
export var survey_answered_for_trip = function (composite_trip, trip_labels_map) {
	Logger.log_debug (__mod__ ('called survey_answered_for_trip for trip %s', composite_trip));
	if (__in__ ('user_input', composite_trip) && __in__ ('trip_user_input', composite_trip ['user_input'])) {
		return composite_trip ['user_input'] ['trip_user_input'] ['data'] ['name'];
	}
	if (trip_labels_map && __in__ (composite_trip ['_id'] ['$oid'], trip_labels_map) && __in__ ('SURVEY', trip_labels_map [composite_trip ['_id'] ['$oid']]) && __in__ ('data', trip_labels_map [composite_trip ['_id'] ['$oid']] ['SURVEY'])) {
		return trip_labels_map [composite_trip ['_id'] ['$oid']] ['SURVEY'] ['data'] ['name'];
	}
	return null;
};
export var get_surveys_summary = function (composite_trips, trip_labels_map, app_config) {
	var surveys_summary = dict ({});
	for (var trip of composite_trips) {
		var prompted_survey = survey_prompted_for_trip (trip, app_config);
		if (!(prompted_survey)) {
			// pass;
			continue;
		}
		if (!__in__ (prompted_survey, surveys_summary)) {
			surveys_summary [prompted_survey] = dict ({'answered': 0, 'unanswered': 0, 'mismatched': 0});
		}
		var answered_survey = survey_answered_for_trip (trip, trip_labels_map);
		if (answered_survey == prompted_survey) {
			surveys_summary [prompted_survey] ['answered']++;
		}
		else if (answered_survey) {
			Logger.log_warn ('Unexpected: trip {} answered survey {} but should have been prompted for {}'.format (trip ['_id'] ['$oid'], answered_survey, prompted_survey));
			surveys_summary [prompted_survey] ['mismatched']++;
		}
		else {
			surveys_summary [prompted_survey] ['unanswered']++;
		}
	}
	return surveys_summary;
};

//# sourceMappingURL=metrics.surveys.surveys_summary.map