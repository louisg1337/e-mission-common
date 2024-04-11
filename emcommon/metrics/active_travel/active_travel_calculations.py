import logger as Logger
from metrics.active_travel.standard_met_mode_map import standard_met_mode_map


def get_mets_mode_map(label_options):
    """
    Gets a mapping of modes to their METs, given label options
    :param label_options: label options dict (from dynamic config 'label_options')
    :return: a dict of modes to their METs
    """
    mode_options = label_options['MODE']
    mode_met_entries = []
    for opt in mode_options:
        if opt.get('met_equivalent'):
            curr_met = standard_met_mode_map[opt['met_equivalent']]
            mode_met_entries.append([opt['value'], curr_met])
        else:
            if opt.get('met'):
                curr_met = opt['met']
                for range_name in curr_met:
                    curr_met[range_name]['range'] = [
                        i if i != -1 else float('inf')
                        for i in curr_met[range_name]['range']
                    ]
                mode_met_entries.append([opt['value'], curr_met])
            else:
                Logger.log_warn(f'Did not find either met_equivalent or met for {opt["value"]} ignoring entry')
    return mode_met_entries
