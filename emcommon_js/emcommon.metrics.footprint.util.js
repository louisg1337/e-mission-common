// Transcrypt'ed from Python, 2024-08-02 08:25:08
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'emcommon.metrics.footprint.util';
export var KWH_PER_GAL_GASOLINE = 33.7;
export var DIESEL_GGE = 0.88;
export var KWH_PER_GAL_DIESEL = KWH_PER_GAL_GASOLINE * 1.14;
export var KWH_PER_GAL_BIODIESEL = KWH_PER_GAL_GASOLINE * 1.05;
export var KWH_PER_GAL_LPG = KWH_PER_GAL_GASOLINE * 0.74;
export var KWH_PER_GAL_CNG = KWH_PER_GAL_GASOLINE * 0.26;
export var KWH_PER_KG_HYDROGEN = KWH_PER_GAL_GASOLINE * 1.0;
export var KWH_PER_GAL_OTHER = KWH_PER_GAL_GASOLINE * 1.0;
export var FUELS_KG_CO2_PER_KWH = dict ({'gasoline': 8.89 / KWH_PER_GAL_GASOLINE, 'diesel': 10.18 / (KWH_PER_GAL_GASOLINE / DIESEL_GGE), 'jet_fuel': 0.25, 'cng': 0.25, 'lpg': 0.25});
export var MI_PER_KM = 0.621371;
export var mpge_to_wh_per_km = function (mpge) {
	return ((MI_PER_KM / mpge) * KWH_PER_GAL_GASOLINE) * 1000;
};
export var year_of_trip = function (trip) {
	return int (trip ['start_fmt_time'].py_split ('-') [0]);
};
export var find_closest_available_year = function (year, available_years) {
	var year = int (year);
	var available_years = (function () {
		var __accu0__ = [];
		for (var y of available_years) {
			__accu0__.append (int (y));
		}
		return __accu0__;
	}) ();
	var diffs = (function () {
		var __accu0__ = [];
		for (var y of available_years) {
			__accu0__.append (abs (y - year));
		}
		return __accu0__;
	}) ();
	return available_years [diffs.index (min (diffs))];
};

//# sourceMappingURL=emcommon.metrics.footprint.util.map