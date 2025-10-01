from datetime import datetime
from datetime import date
import numpy as np 
from scipy.io import loadmat
import pandas as pd

def datenum(d):
    # d - datetime
    return 366 + d.toordinal() + (d - datetime.fromordinal(d.toordinal())).total_seconds()/(24*60*60)


def datenum2000(d):
    # Days since 2000 - jan
    # d - datetime
    return datenum(d) - 730486

def r2r(x):
#     revolutions to radians function
#     input
#     x = argument (revolutions; 0 <= x <= 1)
#     output
#     y = equivalent x (radians; 0 <= y <= 2 pi)
    
    pi = np.pi

    return 2*pi*(x % 1);


def sun_md2000(mjd2000):
    # mjd2000 - result after datenum2000
    pi = np.pi
    
    atr = pi/648000
    
    # time arguments
    djd = mjd2000-0.5

    t = (djd / 36525) + 1
        
    # fundamental arguments (radians)
    
    gs = r2r(0.993126 + 0.0027377785 * djd)
    lm = r2r(0.606434 + 0.03660110129 * djd)
    ls = r2r(0.779072 + 0.00273790931 * djd)
    g2 = r2r(0.140023 + 0.00445036173 * djd)
    g4 = r2r(0.053856 + 0.00145561327 * djd)
    g5 = r2r(0.056531 + 0.00023080893 * djd)
    rm = r2r(0.347343 - 0.00014709391 * djd)
    
    # geocentric, ecliptic longitude of the sun (radians)
    plon = 6910 * np.sin(gs) + 72 * np.sin(2 * gs) - 17 * t * np.sin(gs);
    plon = plon - 7 * np.cos(gs - g5) + 6 * np.sin(lm - ls) + 5 * np.sin(4 * gs - 8 * g4 + 3 * g5)
    plon = plon - 5 * np.cos(2 * (gs - g2)) - 4 * (np.sin(gs - g2) - np.cos(4 * gs - 8 * g4 + 3 * g5))
    plon = plon + 3 * (np.sin(2 * (gs - g2)) - np.sin(g5) - np.sin(2 * (gs - g5)))
    plon = ls + atr * (plon - 17 * np.sin(rm))
    
    # geocentric distance of the sun (kilometers)
    rsm = 149597870.691 * (1.00014 - 0.01675 * np.cos(gs) - 0.00014 * np.cos(2 * gs));
    
    # obliquity of the ecliptic (radians)
    obliq = atr * (84428 - 47 * t + 9 * np.cos(rm))
    
    # geocentric, equatorial right ascension and declination (radians)
    a = np.sin(plon) * np.cos(obliq)
    b = np.cos(plon)
    
    rasc = np.arctan2(a, b);
    decl = np.arcsin(np.sin(obliq) * np.sin(plon))
        
    return rasc, decl