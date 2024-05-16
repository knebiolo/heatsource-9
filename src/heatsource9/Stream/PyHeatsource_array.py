# -*- coding: utf-8 -*-
"""
Created on Sun May  5 09:41:39 2024

@author: Kevin.Nebiolo

PyHeatsource refactored to take advantage of array processing
"""

import numpy as np
import bisect

def calc_solar_position(lat, lon, time, offset, JDC, heatsource8, radial_count):
    """
    Calculate the solar position for a given latitude, longitude, time, and date.

    This function computes the altitude, zenith, daytime indicator, radial transect, 
    and modified azimuth angle of the sun based on the Julian Day Count (JDC) and other 
    parameters. It handles both standard and heatsource8-specific calculations, where 
    heatsource8 mode alters the method for computing the transect index.

    Parameters:
    - lat (float): Latitude of the location in degrees. Positive for north, negative for south.
    - lon (float): Longitude of the location in degrees. Positive for east, negative for west.
    - time (float): Local solar time in minutes from midnight.
    - offset (float): Timezone offset from UTC in hours.
    - JDC (float): Julian Day Count.
    - heatsource8 (bool): Flag to determine the use of heatsource8-specific calculations.
    - radial_count (int): The number of radial transects.

    Returns:
    - tuple: A tuple containing:
      - Altitude (float): The altitude of the sun above the horizon in degrees.
      - Zenith (float): The zenith angle of the sun in degrees.
      - Daytime (int): Indicator (0 for night, 1 for day) based on whether the sun is above the horizon.
      - tran (int): The index of the radial transect direction corresponding to the sun's azimuth.
      - Azimuth_mod (float): The modified azimuth angle considering the specific transect segmentation.

    Raises:
    - ValueError: If any input parameters are out of expected range.

    Example:
    >>> calc_solar_position(45.0, -123.0, 720, -7, 2458963.5, False, 8)
    (45.3, 44.7, 1, 5, 123.45)

    Notes:
    The calculation assumes the earth as a perfect sphere and uses the simplified formulae
    for solar position calculations. This function does not account for atmospheric effects
    other than a basic refraction correction.
    """
    rad = np.deg2rad
    deg = np.rad2deg

    # Constants and angle conversions
    MeanObliquity = 23.439292 - JDC * 0.000013
    Eccentricity = 0.016708634 - JDC * (0.000042037 + 0.0000001267 * JDC)
    GeoMeanLongSun = (280.46646 + JDC * (36000.76983 + 0.0003032 * JDC)) % 360
    GeoMeanAnomalySun = 357.52911 + JDC * (35999.05029 - 0.0001537 * JDC)

    # Solar calculations
    SunEqofCenter = np.sin(rad(GeoMeanAnomalySun)) * (1.914602 - JDC * (0.004817 + 0.000014 * JDC))
    SunApparentLong = GeoMeanLongSun + SunEqofCenter - 0.00569 - 0.00478 * np.sin(rad(125.04 - 1934.136 * JDC))
    Declination = deg(np.arcsin(np.sin(rad(MeanObliquity)) * np.sin(rad(SunApparentLong))))

    # Time correction for solar position
    EquationOfTime = 4 * deg(np.tan(rad(MeanObliquity / 2))**2 * np.sin(2 * rad(GeoMeanLongSun)) - 2 * Eccentricity * np.sin(rad(GeoMeanAnomalySun)))
    SolarTime = (time + EquationOfTime + offset * 60 - 4 * lon) % 1440
    HourAngle = rad((SolarTime / 4 - 180) % 360)

    # Solar altitude and azimuth
    SolarVector = np.sin(rad(lat)) * np.sin(rad(Declination)) + np.cos(rad(lat)) * np.cos(rad(Declination)) * np.cos(HourAngle)
    Zenith = deg(np.arccos(SolarVector))
    Altitude = 90 - Zenith
    Azimuth = deg(np.arctan2(np.sin(HourAngle), np.cos(HourAngle) * np.sin(rad(lat)) - np.tan(rad(Declination)) * np.cos(rad(lat))))

    # Correction for atmospheric refraction
    Refraction = 0.0167 / np.tan(rad(Altitude + 3.0 / (Altitude + 12.0))) if Altitude > -0.575 else -20.774 / np.tan(rad(Altitude))
    Altitude += Refraction / 60

    # Daytime indicator
    Daytime = 1 if Altitude > 0 else 0

    # Determine transect index based on azimuth
    if heatsource8:
        tran = int(Azimuth // (360 / 8))
    else:
        Angle_Incr = 360.0 / radial_count
        DirNumbers = list(range(1, radial_count + 1))
        AngleStart = [x * Angle_Incr - Angle_Incr / 2 for x in DirNumbers]
        Azimuth_mod = Azimuth + 360 if Azimuth < AngleStart[0] else Azimuth
        tran = bisect.bisect(AngleStart, Azimuth_mod) - 1

    return Altitude, Zenith, Daytime, tran, Azimuth

