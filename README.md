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
 

