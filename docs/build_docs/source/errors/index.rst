Common errors
================

Check atoms
--------------

The following error message indicates that the atom(s) you chose to calculate the distance metric or constrain does not exist.


..  code-block:: console

    Check the atoms A:999:C given to calculate the distance metric.

To resolve the issue, you should:

- ensure the atom string has the correct format, i.e. ``"chain_id:residue_number:atom_name"``

- examine the protein structure in Schrödinger Maestro (or open the PDB file as text) and double-check, if the atom exists.

You can easily check residue numbers and atom names in the bottom panel in Maestro by hovering the mouse pointer over a specific atom. In this example, the correct atom string would be ``"A:106:OH"``.

.. image:: ../img/ppi_tutorial_1e.png
  :width: 400
  :align: center


FileNotFound
-------------

If PELE raises ``FileNotFoundError``, it probably means it cannot find one of the files specified in ``input.yaml`` such as system, ligand or RMSD reference. Make sure:

    - there are no spelling mistakes in file names

    - all required files are located in your working directory (or provide a relative path in your input file instead).

..  code-block:: console

    FileNotFoundError: [Errno 2] No such file or directory: '/home/anna/errors/file.pdb'


ValueError - ligand
---------------------

This error indicates that the software was not able to find the ligand in the PDB file. Make sure ``chain`` and ``resname`` flags
in your input file have correct values. Remember that ligands needs to have a unique chain ID!

..  code-block:: console

    ValueError: Something went wrong when extracting the ligand. Check residue&Chain on input

Connections Warning
---------------------

This warning indicates the the PDB file is missing the connectivity section. To resolve the issue, you should import the PDB in Schrödinger Maestro and preprocess it, launching the Protein Preparation Wizard.


Note that **CONECT lines are required for peleffy** forcefield builder.

..  code-block:: console

    pele_platform.Errors.custom_errors.ConnectionsError: Your PDB file is missing the CONECT lines. Please do not remove them after Schrodinger preprocessing.

Parametrization
------------------

Sometimes parametrization of a hetero molecule (cofactor, modified residue, crystallization factor) will fail, which
should result in the following warning message:

..  code-block:: console

    Failed to parametrize residue MET. You can skip it or parametrize manually
    (see documentation: https://nostrumbiodiscovery.github.io/pele_platform/errors/index.html#parametrization).
    The error raised was: Size of atom parameter lists should match.

Remove the residue
+++++++++++++++++++++

If the hetero molecule is **not necessary** to study your system, the easiest way to handle this is to **remove it from the PDB file**. Similarly, you can ignore the warning, but PELE is likely going to crash because it will miss the template.


Parametrize manually
++++++++++++++++++++++++
Alternatively, you can **parametrize the molecule manually** and pass obtained template and rotamer files in the ``input.yaml``.

    1. Save the residue to a separate PDB file, ensure the CONECT lines are included and the Lewis structure is correct.

    2. Run the following command inside the Python environment of the platform to create the default rotamer and template files. For more options, please refer to the `Open Force Field for PELE documentation <https://martimunicoy.github.io/peleffy/usage.html>`_.

    ..  code-block:: console

        python -m peleffy.main ligand.pdb


    3. Add paths to your newly created files to the input.yaml, for example:


    .. code-block:: yaml

        templates:
          - "/path/to/metz"

        rotamers:
          - "/path/to/MET.rot.assign"
