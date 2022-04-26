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

        """
        Class to store variables related to altitude control for the aircraft.

        :param store_PE:  Whether UAV will store excess net power as altitude.
        :param cruise_alt: Cruising altitude.
        :param max_cruise_alt: Maximum cruising altitude.
        :param aoa_init: Initial angle of attack (deg)
        :param aoa_desc: Landing angle of attack (deg)
        :param asc_rate: Ascending rate as a multiplier of cruise power
        :param dsc_rate: Descending rate as a multiplier of cruise power
        """

        self.store_PE = store_PE
        self.cruise_alt = cruise_alt
        self.max_cruise_alt = max_cruise_alt
        self.aoa_init = aoa_init
        self.aoa_desc = aoa_desc
        self.asc_rate = asc_rate
        self.dsc_rate = dsc_rate
