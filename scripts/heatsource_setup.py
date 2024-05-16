# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:55:04 2024

@author: Kevin.Nebiolo
"""
import sys
sys.path.append(r"C:\Users\knebiolo\OneDrive - Kleinschmidt Associates, Inc\Software\heatsource-9\src\heatsource9")

import BigRedButton 

from os.path import join

control_file = 'HeatSource_Control.csv'
model_dir = r'Q:\Client_Data\Other\Chehalis\2_09_RiparianTempOffset\QC1\Heatsource\Mainstem\VMP\inputs'
output_dir = r"C:\Users\knebiolo\Desktop\heatsource\Chehalis\VMP"

# Parameterize the control file and write to csv
BigRedButton.setup_cf(model_dir, control_file, use_timestamp=True, overwrite=False,
                      usertxt="VMP at Mainstem",
                      name="mainstem_vmp",
                      inputdir=join(model_dir, "inputs", ""),
                      outputdir= output_dir,
                      length=64.0,
                      outputkm="all",
                      datastart="06/04/2013",
                      modelstart="06/05/2013",
                      modelend="09/23/2013",
                      dataend="09/24/2013",
                      flushdays=1,
                      offset=-7,
                      dt=0.5,
                      dx=150,
                      longsample=25,
                      bcfile="mainstem_boundary.csv",
                      inflowsites=1,
                      inflowinfiles="mainstem_vmp_tributary.csv",
                      inflowkm="59.2,50.4,34.4,24.8,11.6,10.8,9.6,5.4,5.2,5.0",
                      accretionfile="mainstem_accretion.csv",
                      metsites=1,
                      metfiles="mainstem_meteorology.csv",
                      metkm="0",
                      calcevap="False",
                      evapmethod="Mass Transfer",
                      wind_a=1.51E-09,
                      wind_b=1.6E-09,
                      calcalluvium="False",
                      alluviumtemp=12.0,
                      morphfile="mainstem_morphology.csv",
                      lcdatafile="mainstem_vmp_lc_data.csv",
                      lccodefile="mainstem_vmp_lc_codes.csv",
                      trans_count=8,
                      transsample_count=9,
                      transsample_distance=8,
                      emergent="True",
                      lcdatainput="Codes",
                      canopy_data= "CanopyCover",
                      lcsampmethod="point",
                      heatsource8="True")




