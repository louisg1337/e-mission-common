// Transcrypt'ed from Python, 2024-08-23 15:32:02
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'emcommon.logger';
export var debug = function () {
	var args = tuple ([].slice.apply (arguments).slice (0));
	if (window ['Logger']) {
		window ['Logger'].log (window ['Logger'].LEVEL_DEBUG, ...args);
	}
	else {
		console.log (...args);
	}
};
export var info = function () {
	var args = tuple ([].slice.apply (arguments).slice (0));
	if (window ['Logger']) {
		window ['Logger'].log (window ['Logger'].LEVEL_INFO, ...args);
	}
	else {
		console.info (...args);
	}
};
export var warn = function () {
	var args = tuple ([].slice.apply (arguments).slice (0));
	if (window ['Logger']) {
		window ['Logger'].log (window ['Logger'].LEVEL_WARN, ...args);
	}
	else {
		console.warn (...args);
	}
};
export var error = function () {
	var args = tuple ([].slice.apply (arguments).slice (0));
	if (window ['Logger']) {
		window ['Logger'].log (window ['Logger'].LEVEL_ERROR, ...args);
	}
	else {
		console.error (...args);
	}
};

//# sourceMappingURL=emcommon.logger.map