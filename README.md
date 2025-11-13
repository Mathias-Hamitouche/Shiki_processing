Shiki Processing is made for extra post-processing steps for LC-MS /GC-MS data processing using MZmine.

**What Shiki Processings does :** 

- Atom counting of chemicals formulas determined using MZmine chemical formula determination module
- Calculation O/C, H/C, N/C ratios
- Cleaning up the CSV of all unnecessary columns accumulated through the Batch mode process
- Deleting all features which has undetermined chemical formulas
- Determine the plausibility of chemical formulas using atom ratios and RDBE and delete features with impossible chemical formula :

impossible if : H/C = 0, RDBE < 0, RDBE > C; unlikely if : O/C = 0 and N/C > 0.5, RDBE/C > 0.8; plausible : all of the remaining features 

This script is my first python script I have ever made so feedbacks are heavily appreciated !
