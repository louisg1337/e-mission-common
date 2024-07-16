# This is the entry point for Transcrypt, specifying the Python code that will be transpiled to JavaScript

import emcommon.logger as Logger
import emcommon.metrics.metrics_summaries as metrics_summaries
import emcommon.metrics.surveys.surveys_summary as surveys_summary
import emcommon.metrics.carbon.carbon_calculations as carbon_calculations
import emcommon.metrics.active_travel.active_travel_calculations as active_travel_calculations
import emcommon.survey.conditional_surveys as conditional_surveys
import emcommon.bluetooth.ble_matching as ble_matching
import emcommon.metrics.footprint_calculations as footprint_calculations

def dict_to_js_obj(py_dict):
    """
    Converts a Python dictionary to a JavaScript object
    """
    js_obj = {} # __: jsiter
    for key, value in py_dict.items():
        if isinstance(value, dict):
            js_obj[key] = dict_to_js_obj(value)
        else:
            js_obj[key] = value
    return js_obj
