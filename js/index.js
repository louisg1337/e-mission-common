import * as TranslatedCode from './__translated_src__/__init__.js';

/**
 * @description Converts a Python dict object to a plain JS object
 * @param {*} pythonDict A Python dict object, coming from Python code that was transpiled to JS by Transcrypt
 */
export const dictToObj = (pythonDict) =>
  Object.fromEntries(Object.entries(pythonDict));

export const CarbonCalculations = TranslatedCode.CarbonCalculations;
export const MetricsSummaries = TranslatedCode.MetricsSummaries;
