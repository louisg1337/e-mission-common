import emcommon.logger as Logger
from emcommon.metrics.footprint.footprint_calculations import mpge_to_wh_per_km

mode_colors = {
    "pink": '#c32e85', # oklch(56% 0.2 350)     # e-car
    "red": '#c21725', # oklch(52% 0.2 25)      # car
    "orange": '#bf5900', # oklch(58% 0.16 50)     # air, hsr
    "green": '#008148', # oklch(53% 0.14 155)    # bike, e-bike, moped
    "blue": '#0074b7', # oklch(54% 0.14 245)    # walk
    "periwinkle": '#6356bf', # oklch(52% 0.16 285)    # light rail, train, tram, subway
    "magenta": '#9240a4', # oklch(52% 0.17 320)    # bus
    "grey": '#555555', # oklch(45% 0 0)         # unprocessed / unknown
    "taupe": '#7d585a', # oklch(50% 0.05 15)     # ferry, trolleybus, user-defined modes
}

NON_ACTIVE_METS = {
    "ALL": {"range": [0, float('inf')]},
}
WALKING_METS = {
    "VERY_SLOW": {"range": [0, 2.0], "mets": 2.0},
    "SLOW": {"range": [2.0, 2.5], "mets": 2.8},
    "MODERATE_0": {"range": [2.5, 2.8], "mets": 3.0},
    "MODERATE_1": {"range": [2.8, 3.2], "mets": 3.5},
    "FAST": {"range": [3.2, 3.5], "mets": 4.3},
    "VERY_FAST_0": {"range": [3.5, 4.0], "mets": 5.0},
    "VERY_FAST_1": {"range": [4.0, 4.5], "mets": 6.0},
    "VERY_VERY_FAST": {"range": [4.5, 5], "mets": 7.0},
    "SUPER_FAST": {"range": [5, 6], "mets": 8.3},
    "RUNNING": {"range": [6, float('inf')], "mets": 9.8},
}
BIKING_METS = {
    "VERY_VERY_SLOW": {"range": [0, 5.5], "mets": 3.5},
    "VERY_SLOW": {"range": [5.5, 10], "mets": 5.8},
    "SLOW": {"range": [10, 12], "mets": 6.8},
    "MODERATE": {"range": [12, 14], "mets": 8.0},
    "FAST": {"range": [14, 16], "mets": 10.0},
    "VERT_FAST": {"range": [16, 19], "mets": 12.0},
    "RACING": {"range": [20, float('inf')], "mets": 15.8},
}
E_BIKING_METS = {
    "ALL": {"range": [0, float('inf')], "mets": 4.9}
}

# "average" values for various modes of transportation
# TODO get these from GREET or somewhere trustworthy
GAS_CAR_MPG = 24
ECAR_MPGE = 100
PHEV_UF = 0.4 # UF = utility factor
PHEV_GAS_MPG = 40
PHEV_ELEC_MPGE = 100
E_BIKE_WH_PER_KM = 13.67
E_SCOOTER_WH_PER_KM = 16.78
MOPED_AVG_MPG = 100
TAXI_WH_PER_KM = 941.5
AIR_WH_PER_KM = 999

AIR_FOOTPRINT = { "jet_fuel": { "wh_per_km": AIR_WH_PER_KM } }
CAR_FOOTPRINT = { "gasoline": { "wh_per_km": mpge_to_wh_per_km(GAS_CAR_MPG) } }
E_CAR_FOOTPRINT = { "electric": { "wh_per_km": mpge_to_wh_per_km(ECAR_MPGE) } }
PHEV_CAR_FOOTPRINT = {
    "electric": {
        "wh_per_km": mpge_to_wh_per_km(PHEV_ELEC_MPGE),
        "weight": PHEV_UF
    },
    "gasoline": {
        "wh_per_km": mpge_to_wh_per_km(PHEV_GAS_MPG),
        "weight": 1 - PHEV_UF
    },
}
E_BIKE_FOOTPRINT = {"electric": {"wh_per_km": E_BIKE_WH_PER_KM }}
E_SCOOTER_FOOTPRINT = { "electric": { "wh_per_km": E_SCOOTER_WH_PER_KM } }
MOPED_FOOTPRINT = { "gasoline": { "wh_per_km": mpge_to_wh_per_km(MOPED_AVG_MPG) } }
TAXI_FOOTPRINT = { "gasoline": { "wh_per_km": TAXI_WH_PER_KM } }

BASE_MODES = {
  # BEGIN MotionTypes
  "IN_VEHICLE": {
      "icon": 'speedometer',
      "color": mode_colors['red'],
      "met": NON_ACTIVE_METS,
      # footprint not known; left undefined. later filled in by an average of:
      # CAR, BUS, LIGHT_RAIL, TRAIN, TRAM, SUBWAY
  },
  "BICYCLING": {
      "icon": 'bike',
      "color": mode_colors['green'],
      "met": BIKING_METS,
      "footprint": {},
  },
  "ON_FOOT": {
      "icon": 'walk',
      "color": mode_colors['blue'],
      "met": WALKING_METS,
      "footprint": {},
  },
  "UNKNOWN": {
      "icon": 'help',
      "color": mode_colors['grey'],
      # met and footprint not known; left undefined
  },
  "WALKING": {
      "icon": 'walk',
      "color": mode_colors['blue'],
      "met": WALKING_METS,
      "footprint": {},
  },
  "AIR_OR_HSR": {
      "icon": 'airplane',
      "color": mode_colors['orange'],
      "met": NON_ACTIVE_METS,
      "footprint": AIR_FOOTPRINT,
  },
  # END MotionTypes
  "CAR": {
      "icon": 'car',
      "color": mode_colors['red'],
      "met": NON_ACTIVE_METS,
      "footprint": CAR_FOOTPRINT,
  },
  "E_CAR": {
      "icon": 'car-electric',
      "color": mode_colors['pink'],
      "met": NON_ACTIVE_METS,
      "footprint": E_CAR_FOOTPRINT,
  },
  "PHEV_CAR": {
      "icon": 'car-electric',
      "color": mode_colors['pink'],
      "met": NON_ACTIVE_METS,
      "footprint": PHEV_CAR_FOOTPRINT,
  },
  "E_BIKE": {
      "icon": 'bicycle-electric',
      "color": mode_colors['green'],
      "met": E_BIKING_METS,
      "footprint": E_BIKE_FOOTPRINT,
  },
  "E_SCOOTER": {
      "icon": 'scooter-electric',
      "color": mode_colors['periwinkle'],
      "met": NON_ACTIVE_METS,
      "footprint": E_SCOOTER_FOOTPRINT,
  },
  "MOPED": {
      "icon": 'moped',
      "color": mode_colors['green'],
      "met": NON_ACTIVE_METS,
      "footprint": MOPED_FOOTPRINT,
  },
  "TAXI": {
      "icon": 'taxi',
      "color": mode_colors['red'],
      "met": NON_ACTIVE_METS,
      "footprint": TAXI_FOOTPRINT,
  },
  "BUS": {
      "icon": 'bus-side',
      "color": mode_colors['magenta'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["MB", "RB", "CB"] }, # fixed-route bus, bus rapid transit, commuter bus
  },
  "AIR": {
      "icon": 'airplane',
      "color": mode_colors['orange'],
      "met": NON_ACTIVE_METS,
      "footprint": AIR_FOOTPRINT,
  },
  "LIGHT_RAIL": {
      "icon": 'train-car-passenger',
      "color": mode_colors['periwinkle'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["LR"] } # light rail
  },
  "TRAIN": {
      "icon": 'train-car-passenger',
      "color": mode_colors['periwinkle'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["HR", "YR"] } # heavy rail, hybrid rail
  },
  "TRAM": {
      "icon": 'tram',
      "color": mode_colors['periwinkle'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["SR"] } # streetcar
  },
  "SUBWAY": {
      "icon": 'subway-variant',
      "color": mode_colors['periwinkle'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["HR"] } # heavy rail
  },
  "FERRY": {
      "icon": 'ferry',
      "color": mode_colors['taupe'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["FB"] } # ferry boat
  },
  "TROLLEYBUS": {
      "icon": 'bus-side',
      "color": mode_colors['taupe'],
      "met": NON_ACTIVE_METS,
      "footprint": { "transit": ["TB", "SR"] } # trolleybus, streetcar
  },
  "UNPROCESSED": {
      "icon": 'help',
      "color": mode_colors['grey'],
      # met not known; left undefined
      # footprint not known; left undefined
  },
  "OTHER": {
      "icon": 'pencil-circle',
      "color": mode_colors['taupe'],
      # met not known; left undefined
      # footprint not known; left undefined
  },
};

def get_base_mode_by_key(motionName):
    key = ('' + motionName).upper()
    pop = key.split('.').pop() # if "MotionTypes.WALKING", then just take "WALKING"
    return BASE_MODES.get(pop, BASE_MODES["UNKNOWN"])


def get_rich_mode(label_option):
    """
    A "label_option" is one of the mode options given by a deployer in the label_options config
    It can extend on a base mode, override props, or borrow "equivalent" props from another base mode
    :param label_option: a dict with partial, full, or extended mode properties
    :return: a rich mode object with all the properties filled in
    e.g. get_rich_mode({ "base_mode": "WALKING", "color": "#000000" })
    -> { "icon": "walk", "color": "#000000", "met": WALKING_METS, "footprint": {} }
    """
    Logger.log_debug(f"Getting rich mode for label_option: {label_option}")
    rich_mode = {}
    base_props = ['icon', 'color', 'met', 'footprint']
    for prop in base_props:
        if prop in label_option:
            rich_mode[prop] = label_option[prop]
        elif f"{prop}_equivalent" in label_option:
            import emcommon.diary.base_modes as emcdb
            rich_mode[prop] = emcdb.get_base_mode_by_key(label_option[f"{prop}_equivalent"])[prop]
        else:
            # backwards compat for camelCase; eventually want to standardize to snake_case
            for bm in ['base_mode', 'baseMode']: 
                if bm in label_option:
                    rich_mode[prop] = get_base_mode_by_key(label_option[bm])[prop]
    Logger.log_debug(f"Rich mode: {rich_mode}")
    return rich_mode
