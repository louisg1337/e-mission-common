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

BASE_MODES = {
  # BEGIN MotionTypes
  "IN_VEHICLE": { "name": 'IN_VEHICLE', "icon": 'speedometer', "color": mode_colors["red"] },
  "BICYCLING": { "name": 'BICYCLING', "icon": 'bike', "color": mode_colors["green"] },
  "ON_FOOT": { "name": 'ON_FOOT', "icon": 'walk', "color": mode_colors["blue"] },
  "UNKNOWN": { "name": 'UNKNOWN', "icon": 'help', "color": mode_colors["grey"] },
  "WALKING": { "name": 'WALKING', "icon": 'walk', "color": mode_colors["blue"] },
  "AIR_OR_HSR": { "name": 'AIR_OR_HSR', "icon": 'airplane', "color": mode_colors["orange"] },
  # END MotionTypes
  "CAR": { "name": 'CAR', "icon": 'car', "color": mode_colors["red"] },
  "E_CAR": { "name": 'E_CAR', "icon": 'car-electric', "color": mode_colors["pink"] },
  "E_BIKE": { "name": 'E_BIKE', "icon": 'bicycle-electric', "color": mode_colors["green"] },
  "E_SCOOTER": { "name": 'E_SCOOTER', "icon": 'scooter-electric', "color": mode_colors["periwinkle"] },
  "MOPED": { "name": 'MOPED', "icon": 'moped', "color": mode_colors["green"] },
  "TAXI": { "name": 'TAXI', "icon": 'taxi', "color": mode_colors["red"] },
  "BUS": { "name": 'BUS', "icon": 'bus-side', "color": mode_colors["magenta"] },
  "AIR": { "name": 'AIR', "icon": 'airplane', "color": mode_colors["orange"] },
  "LIGHT_RAIL": { "name": 'LIGHT_RAIL', "icon": 'train-car-passenger', "color": mode_colors["periwinkle"] },
  "TRAIN": { "name": 'TRAIN', "icon": 'train-car-passenger', "color": mode_colors["periwinkle"] },
  "TRAM": { "name": 'TRAM', "icon": 'fas fa-tram', "color": mode_colors["periwinkle"] },
  "SUBWAY": { "name": 'SUBWAY', "icon": 'subway-variant', "color": mode_colors["periwinkle"] },
  "FERRY": { "name": 'FERRY', "icon": 'ferry', "color": mode_colors["taupe"] },
  "TROLLEYBUS": { "name": 'TROLLEYBUS', "icon": 'bus-side', "color": mode_colors["taupe"] },
  "UNPROCESSED": { "name": 'UNPROCESSED', "icon": 'help', "color": mode_colors["grey"] },
  "OTHER": { "name": 'OTHER', "icon": 'pencil-circle', "color": mode_colors["taupe"] },
};

def get_base_mode_by_key(motionName):
    key = ('' + motionName).upper()
    pop = key.split('.').pop() # if "MotionTypes.WALKING", then just take "WALKING"
    return BASE_MODES.get(pop, BASE_MODES["UNKNOWN"])