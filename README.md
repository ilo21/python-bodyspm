## Python code for analysing body maps

This is a experimental version of python code that can be used instead of or in addition to (Matlab-based) BodySPM by Enrico Glerean (a version of matlab-based BodySPM is available at https://version.aalto.fi/gitlab/eglerean/sensations). 
It is designed to work with data coming from a version of https://version.aalto.fi/gitlab/eglerean/embody . 

### Functionality
#### Pre-processing
 - read in the data from theonline data collection system, and converts the topographies to .csv (with each cell representing one pixel). 
 - additional subject info and info about the stimuli is saved as JSONs. (Csv and JSON should be suitable for long term data storage and cross-platform compatibility)
 - combine data from multiple subjects into one hdf5 file for analysis

#### Analysis
 - pixel-wise one sample t-test
 - pixel-wise comparison of two groups, either using two sample t-test or z test of proportions
 - count pixels within a given mask (e.g. within body outline)
 - correlate maps with background variables (e.g. age)

#### Utilities
 - draw single subject colouring within mask
 - draw single subject colouring as-collected (useful for visual quality control)
 - easy multiple comparison correction to use with pixel-wise analyses
 - binarise maps to coloured/not coloured
 
#### Upcoming / planned additions
 - Region of Interest analyses (currently exists as a script, to be converted to a function)
 - correlate two maps with one another / other similarity measure
 - potentially functions for visualising analysis outputs? (currently all except single subject visualisations are done as scripts)


Thanks for a productive meeting! Here’s a suggested step-by-step plan for you Ilona, so that you can get a sense of what functions are available on the repo https://github.com/jtsuvile/python-bodyspm

1. Read in all data (s0_preprocess.py)
2. Make quality control figures for all participants and visually inspect them (you can send them around to all of us to check if you want to, I have some idea of what is “typical” colouring pattern and what is not): function make_qc_figures in bodyfunctions.py
-> trust me, we want to do that before we do the other analyses, since we may need to exclude participants if they did something cray-cray with the colouring and with these sample sizes it could easily impact the end result
3. Make combined emotion maps (like the ones I showed in the meeting): approximately like this https://github.com/jtsuvile/python-bodyspm/blob/endometriosis/emotion_maps_manuscript_fig.py
4. Count pixels per image (for further analysis): something like this https://github.com/jtsuvile/python-bodyspm/blob/endometriosis/s1_count_pixels.py 
5. The output from pixel count will be a happy little csv (per group, ie one for controls and one for patients), anyone can combine & analyse the group differences using the tool they feel most comfortable with (I use R, you could also use SPSS, SAS etc)
