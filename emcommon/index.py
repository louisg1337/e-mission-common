# This is the entry point for Transcrypt, specifying the Python code that will be transpiled to JavaScript

import logger as Logger
import metrics.metrics_summaries as metrics_summaries
import metrics.surveys.surveys_summary as surveys_summary
import metrics.carbon.carbon_calculations as carbon_calculations
import metrics.active_travel.active_travel_calculations as active_travel_calculations
import survey.conditional_surveys as conditional_surveys

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
