
# https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references

KWH_PER_GAL_GASOLINE = 33.7  # from the EPA, used as the basis for MPGe
DIESEL_GGE = 0.88  # .88 gal diesel ≈ 1 gal gasoline
KWH_PER_GAL_DIESEL = KWH_PER_GAL_GASOLINE * 1.14
# GGE constants found from https://epact.energy.gov/fuel-conversion-factors
KWH_PER_GAL_BIODIESEL = KWH_PER_GAL_GASOLINE * 1.05
KWH_PER_GAL_LPG = KWH_PER_GAL_GASOLINE * .74
KWH_PER_GAL_CNG = KWH_PER_GAL_GASOLINE * .26
KWH_PER_KG_HYDROGEN = KWH_PER_GAL_GASOLINE * 1.00
KWH_PER_GAL_OTHER = KWH_PER_GAL_GASOLINE * 1.00 # TODO find a better default value

FUELS_KG_CO2_PER_KWH = {
    # 8.89 kg CO2 / gal (EPA)
    'gasoline': 8.89 / KWH_PER_GAL_GASOLINE,
    # 10.18 kg CO2 / gal (EPA)
    'diesel': 10.18 / (KWH_PER_GAL_GASOLINE / DIESEL_GGE),
    # 0.25 kg CO2 / kWh (https://www.eia.gov/environment/emissions/co2_vol_mass.php)
    'jet_fuel': 0.25,

    'cng': 0.25, # TODO !!
    'lpg': 0.25, # TODO !!
}

MI_PER_KM = 0.621371


def mpge_to_wh_per_km(mpge: float) -> float:
  """
  Convert miles per gallon of gasoline equivalent (MPGe) to watt-hours per kilometer.
  e.g. mpge_to_wh_per_km(100) -> 209.40202700000003
  """
  return MI_PER_KM / mpge * KWH_PER_GAL_GASOLINE * 1000
