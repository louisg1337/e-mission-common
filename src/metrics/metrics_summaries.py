# from util import memoize
import logger as Logger


# @memoize
def labeled_mode_for_trip(composite_trip: dict, trip_labels_map: dict[str, any]) -> str:
    """
    :param composite_trip: composite trip
    :param trip_labels_map: trip labels map
    :return: labeled mode for the trip, derived from the trip's user_input if available, or the trip_labels_map if available, or 'unlabeled' otherwise
    """
    UNLABELED = 'unlabeled'
    if not composite_trip:
        return UNLABELED
    if 'user_input' in composite_trip and 'mode_confirm' in composite_trip['user_input']:
        return composite_trip['user_input']['mode_confirm']
    if trip_labels_map and composite_trip['_id']['$oid'] in trip_labels_map:
        if 'MODE' in trip_labels_map[composite_trip['_id']['$oid']]:
            return trip_labels_map[composite_trip['_id']['$oid']]['MODE']['data']['label']
    return UNLABELED


# @memoize
def generate_summaries(metrics: list[str], composite_trips: list, trip_labels_map: dict[str, any]):
    return {metric: get_summary_for_metric(metric, composite_trips, trip_labels_map) for metric in metrics}


def value_of_metric_for_trip(metric: str, trip: dict, trip_labels_map: dict[str, any]):
    if metric == 'distance':
        return trip['distance']
    elif metric == 'count':
        return 1
    elif metric == 'duration':
        return trip['duration']
    return None


def get_summary_for_metric(metric: str, composite_trips: list, trip_labels_map: dict[str, any]):
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


def metric_summary_by_mode(metric: str, composite_trips: list, trip_labels_map: dict[str, any]):
    """
    :param composite_trips: list of composite trips
    :return: a dict of mode keys to the metric total for that mode
    """
    mode_to_metric_map = {}
    if not composite_trips:
        return mode_to_metric_map
    for trip in composite_trips:
        mode_key = 'mode_' + labeled_mode_for_trip(trip, trip_labels_map)
        if mode_key not in mode_to_metric_map:
            mode_to_metric_map[mode_key] = 0
        mode_to_metric_map[mode_key] += value_of_metric_for_trip(
            metric, trip, trip_labels_map)
    return mode_to_metric_map
