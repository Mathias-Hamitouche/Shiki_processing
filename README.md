Shiki Processing is made for extra post-processing steps for LC-MS /GC-MS data processing using MZmine.

**What Shiki Processings does :** 

- Atom counting of chemicals formulas determined using MZmine chemical formula determination module
- Calculation O/C, H/C, N/C ratios
- Cleaning up the CSV of all unnecessary columns accumulated through the Batch mode process
- Deleting all features which has undetermined chemical formulas
- Determine the plausibility of chemical formulas using atom ratios and RDBE and delete features with impossible chemical formula :

              - impossible if : C <= 0, if H < 0 or H > 2 * C + N + 2 (maximum hydrogen rule), RDBE > C, if N/C > 3, S/C > 2, O/C > 4
              - unlikely if :  3.2 < H/C or H/C < 0.3, 1.2 < O/C or O/C < 0, N/C > 0.4, RDBE/C > 0.5
              - plausible : all of the remaining features 


- Creates a mgf file for molecular networking depending on the analysis

            - GC-EI-MS : creates pseudo MS/MS based on mass spectras with similar retention time (delta RT = 0.1 min)
            - LS-ESI-MS/MS : gets the real MS/MS but only with features that made it through the script filtering
            - LS-ESI-MS : No .mgf file generated

  This script is my first python script I have ever made so feedbacks are heavily appreciated !

Contact at mathias.hamitouche@univ-poitiers.fr
