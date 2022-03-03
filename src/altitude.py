class AltitudeController:
    def __init__(self,
                 store_PE: bool,
                 cruise_alt: float,
                 max_cruise_alt: float,
                 aoa_init: float,
                 aoa_desc: float,
                 asc_rate: float,
                 dsc_rate: float,
                 ):

        self.store_PE = store_PE  # Whether UAV will store excess net power as altitude
        self.cruise_alt = cruise_alt
        self.max_cruise_alt = max_cruise_alt
        self.aoa_init = aoa_init  # Initial angle of attack (deg)
        self.aoa_desc = aoa_desc
        self.asc_rate = asc_rate  # Ascending rate as a multiplier of cruise power
        self.dsc_rate = dsc_rate  # Descending rate as a multiplier of cruise power
