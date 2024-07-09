modeColors = {
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

BaseModes = {
  # BEGIN MotionTypes
  "IN_VEHICLE": { "name": 'IN_VEHICLE', "icon": 'speedometer', "color": modeColors.red },
  "BICYCLING": { "name": 'BICYCLING', "icon": 'bike', "color": modeColors.green },
  "ON_FOOT": { "name": 'ON_FOOT', "icon": 'walk', "color": modeColors.blue },
  "UNKNOWN": { "name": 'UNKNOWN', "icon": 'help', "color": modeColors.grey },
  "WALKING": { "name": 'WALKING', "icon": 'walk', "color": modeColors.blue },
  "AIR_OR_HSR": { "name": 'AIR_OR_HSR', "icon": 'airplane', "color": modeColors.orange },
  # END MotionTypes
  "CAR": { "name": 'CAR', "icon": 'car', "color": modeColors.red },
  "E_CAR": { "name": 'E_CAR', "icon": 'car-electric', "color": modeColors.pink },
  "E_BIKE": { "name": 'E_BIKE', "icon": 'bicycle-electric', "color": modeColors.green },
  "E_SCOOTER": { "name": 'E_SCOOTER', "icon": 'scooter-electric', "color": modeColors.periwinkle },
  "MOPED": { "name": 'MOPED', "icon": 'moped', "color": modeColors.green },
  "TAXI": { "name": 'TAXI', "icon": 'taxi', "color": modeColors.red },
  "BUS": { "name": 'BUS', "icon": 'bus-side', "color": modeColors.magenta },
  "AIR": { "name": 'AIR', "icon": 'airplane', "color": modeColors.orange },
  "LIGHT_RAIL": { "name": 'LIGHT_RAIL', "icon": 'train-car-passenger', "color": modeColors.periwinkle },
  "TRAIN": { "name": 'TRAIN', "icon": 'train-car-passenger', "color": modeColors.periwinkle },
  "TRAM": { "name": 'TRAM', "icon": 'fas fa-tram', "color": modeColors.periwinkle },
  "SUBWAY": { "name": 'SUBWAY', "icon": 'subway-variant', "color": modeColors.periwinkle },
  "FERRY": { "name": 'FERRY', "icon": 'ferry', "color": modeColors.taupe },
  "TROLLEYBUS": { "name": 'TROLLEYBUS', "icon": 'bus-side', "color": modeColors.taupe },
  "UNPROCESSED": { "name": 'UNPROCESSED', "icon": 'help', "color": modeColors.grey },
  "OTHER": { "name": 'OTHER', "icon": 'pencil-circle', "color": modeColors.taupe },
};

def getBaseModeByKey(motionName):
    key = ('' + motionName).toUpperCase()
    pop = key.split('.').pop() # if "MotionTypes.WALKING", then just take "WALKING"
    return (pop and BaseModes[pop]) or BaseModes["UNKNOWN"]