Versions
############

v1.6.0 beta 5
==============

- Interaction restrictions

- Integrate peleffy and support OpenFF force fields

- New module and API for analysis

- Integrate Mean Shift and HDBSCAN clustering algorithms

- Add water sites analysis

- Support for PELE installations on docker and singularity containers

- Support for growing custom fragment libraries

- Kernel density estimator plots

- Constraints levels for alpha carbons

- Changes to Monte Carlo default parameters for some packages

- Allosteric package renamed to site finder

- Minor changes to folder structure

- Better handling of YAML errors

- Optimisation of coordinates parser and bugfixes

- Recover restart flag to allow the users to manually curate control files and use them in a new run

- Support for the new equilibration mode flag of Adaptive

- Fix problems with the box of the Out --> In package

- Add user warnings to facilitate the system preparation

- Introduced flexible filtering of output structures taken into account during analysis.

- Support for conformation perturbation.

- Support for the new PELE minimum steps.

- Other minor improvements


v1.5.1
==========================

- AquaPELE

- High-throughput fragment screening

- Improved out-in exploration

- Support for non-standard residues

- Automatic metal constraints

- Metal polarisation

- Tutorials

- Outliers removed from plots

- Improved documentation


v1.5.0
==========================

- PPI package

- Site finder (pocket exploration) package

- GPCR orthosteric package

- Binding package

- External metal constraints

- Add n random water to your simulation by setting n_waters flag

- More robust error handling

- Remove support python 3.6 and update features python 3.7

- Full refactor of code

- Improvement of frag_pele

- New docs

- Coverage up to 94%


v1.4.4
=====================

- Include further testing of alignment and rdkit symmetry problem

- Include more flags for FragPele

- Improve exceptions with custom errors


v1.4.3
======================

- Fix rdkit substructure search symmetry problem by alignment


v1.4.2
====================

- FragPELE better tested

- Coverage Platform up to 90%

- Pyyaml checker for unexisting keywords in input

- Improve substructure search on symmetric cases

- Minor fixes


v1.4.1
======================

- Wrongly updated


v1.4.0
=======================

- FragPELE supported (Beta-version)

- PPI simulation supported. Global exploration + induced fit (Beta-version)

- Make Platform work through SCHRODINGER and PELE environment variables

- Get rid of PyMol as external dependency

- Use can define several inputs with asterics. i.e. "complex*.pdb"

- Fix bug on dimer constraints only detecting one chain

- Fix other minor bugs

- Better coverage (77%)


v1.3.4
=======================

- Make mae flag convert clusters as well as top poses to mae

- Let user choose number of clusters through analysis_nclust flag

- Allow user to specify the columns of the report via be_column, te_column and limit_column.


v1.3.3
=======================

- Include only analysis flag


v1.3.2
=======================

- Automatically score the simulation by making the average of the 25% best energy structures.

- Reorder top energy structures

- Support conda deployment for python 3.8


v1.3.1
=======================

- Fixed bug in xtc analysis

- Renew environment on SCHRODINGER subprocess


v1.3.0 
=======================

- Set constraints by smiles

- Include a default posprocessing module with plots, top poses and clusters
  
- Separate between AdaptivePELE induced fit (induced_fit_fast) and PELE indeced fit (induced_fit_exhaustive)

- Include skip_ligand_prep option to jump PlopRotTemp missing residue

- Give option ot the user to specify the atom_dist by chain:resname:atomname (A:125:CA)

- Give option mae to transform the best structures to mae files with the metrics as properties

- Fix minor bugs


v1.2.3
=======================

- Automatic PCA mode

- Fix minor bug on global exploration

- Set PPP as external dependence


v1.2.2
=======================

- Fix global exploration bug when joining ligand & receptor

- Add rescoring feature to local a single minimum

- Add induce_fit mode and exploration mode within water_lig parameters to explore hydration sites without moving the ligand or while making the entrance of the ligand.

- Some minor fixes


v1.2.1
=======================

- Add verboseMode

- Add waterPELE and set defaults as we did on WaterMC paper

- Include executable path, data and documents overwriting all constants.py

- Minor fixes


v1.2.0
=======================

- Conda installation

- Insert AdaptivePELE as external dependency

- Fix minor bugs


v1.1.0
=======================

- Automatic Platform to automatically launch PELE&adaptivePELE. It creates the forcefield parameters, the control files, the PELE input.pdb and finally launch the simulation.

- Flexibility to include MSM and Frag PELE

- Flexibility to include analysis scripts

- Flexibility to include PELE modes
