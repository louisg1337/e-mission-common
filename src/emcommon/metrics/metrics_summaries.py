from __future__ import annotations # __: skip
# from util import memoize
import emcommon.logger as Logger


# @memoize
def label_for_trip(composite_trip: dict, label_key: str, trip_labels_map: dict[str, any] = None) -> str:
    """
    :param composite_trip: composite trip
    :param label_key: which type of label to get ('mode', 'purpose', or 'replaced_mode')
    :param trip_labels_map: trip labels map
    :return: the label for the trip, derived from the trip's user_input if available, or the trip_labels_map if available, or 'unlabeled' otherwise
    """
    label_key = label_key.upper()
    label_key_confirm = label_key.lower() + '_confirm'
    UNLABELED = 'unlabeled'
    if not composite_trip:
        return UNLABELED
    if 'user_input' in composite_trip and label_key_confirm in composite_trip['user_input']:
        return composite_trip['user_input'][label_key_confirm]
    if trip_labels_map and composite_trip['_id']['$oid'] in trip_labels_map:
        if label_key_upper in trip_labels_map[composite_trip['_id']['$oid']]:
            return trip_labels_map[composite_trip['_id']['$oid']][label_key_upper]['data']['label']
    return UNLABELED

def labeled_purpose_for_trip(composite_trip: dict, trip_labels_map: dict[str, any] = None) -> str:
    """
    :param composite_trip: composite trip
    :param trip_labels_map: trip labels map
    :return: labeled purpose for the trip, derived from the trip's user_input if available, or the trip_labels_map if available, or 'unlabeled' otherwise
    """
    UNLABELED = 'unlabeled'
    if not composite_trip:
        return UNLABELED
    if 'user_input' in composite_trip and 'purpose_confirm' in composite_trip['user_input']:
        return composite_trip['user_input']['purpose_confirm']
    if trip_labels_map and composite_trip['_id']['$oid'] in trip_labels_map:
        if 'PURPOSE' in trip_labels_map[composite_trip['_id']['$oid']]:
            return trip_labels_map[composite_trip['_id']['$oid']]['PURPOSE']['data']['label']
    return UNLABELED


# @memoize
def generate_summaries(metrics: list[str], composite_trips: list, trip_labels_map: dict[str, any]):
    return {metric: get_summary_for_metric(metric, composite_trips, trip_labels_map) for metric in metrics}


def value_of_metric_for_trip(metric: str, trip: dict):
    if metric == 'distance':
        return trip['distance']
    elif metric == 'count':
        return 1
    elif metric == 'duration':
        return trip['duration']
    return None


def get_summary_for_metric(metric: str, composite_trips: list, trip_labels_map: dict[str, any] = None):
    days_of_metrics_data = {}
    for trip in composite_trips:
        date = trip['start_fmt_time'].split('T')[0]
        if date not in days_of_metrics_data:
            days_of_metrics_data[date] = []
        days_of_metrics_data[date].append(trip)

    days_summaries = []
    for date, trips in days_of_metrics_data.items():
        summary_for_day = {
            'date': date,
        }
        summary_for_day.update(metric_summary_by_mode(
            metric, trips, trip_labels_map))
        days_summaries.append(summary_for_day)
    return days_summaries

def metric_summary_by_mode(metric: str, composite_trips: list, trip_labels_map = None):
    """
    :param composite_trips: list of composite trips
    :return: a dict of mode keys to the metric total for that mode
    """
    grouping_fields = {
        'mode_confirm': lambda trip: label_for_trip(trip, 'mode', trip_labels_map),
        'purpose_confirm': lambda trip: label_for_trip(trip, 'purpose', trip_labels_map),
        'replaced_mode_confirm': lambda trip: label_for_trip(trip, 'replaced_mode', trip_labels_map),
    }

    mode_to_metric_map = {}
    if not composite_trips:
        return mode_to_metric_map
    for trip in composite_trips:
        for grouping_field, field_for_trip_fn in grouping_fields.items():
            grouping_key = grouping_field + '_' + field_for_trip_fn(trip)
            if grouping_key not in mode_to_metric_map:
                mode_to_metric_map[grouping_key] = 0
            mode_to_metric_map[grouping_key] += value_of_metric_for_trip(metric, trip)
    return mode_to_metric_map
