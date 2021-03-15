"""
This module contains classes and methods to handle data coming from PELE
trajectories.
"""


class DataHandler(object):
    """
    Main class to handle data coming from PELE trajectories.
    """
    _NON_METRIC_LABELS = {'#Task', 'Step', 'trajectory', 'epoch',
                          'numberOfAcceptedPeleSteps'}
    _TRAJECTORY_LABEL = 'trajectory'

    def __init__(self, sim_path, report_name, trajectory_name,
                 be_column=None):
        """
        It initializes a DataHandler object.

        Parameters
        ----------
        sim_path : str
            The simulation path containing the output files coming from
            PELE
        report_name : str
            The name of PELE report files
        trajectory_name : str
            The name of PELE trajectory files
        be_column : int
            The column that belongs to the Interaction energy metric in
            PELE report files. Default is None
        """
        self._sim_path = sim_path
        self._report_name = report_name
        self._trajectory_name = trajectory_name
        self._be_column = be_column
        self._dataframe = None

    @classmethod
    def from_parameters(cls, parameters):
        """
        It initializes a DataHandler object from a Parameters object.

        Parameters
        ----------
        parameters : a Parameters object
            The Parameters object containing the parameters that belong
            to the simulation

        Returns
        -------
        data_handler : a DataHandler object
            The DataHandler object obtained from the parameters that were
            supplied
        """
        import os

        sim_path = os.path.join(parameters.pele_dir,
                                parameters.output)
        report_name = parameters.report_name
        trajectory_name = parameters.traj_name
        be_column = parameters.be_column

        data_handler = DataHandler(sim_path, report_name, trajectory_name,
                                   be_column)

        return data_handler

    @classmethod
    def from_dataframe(cls, dataframe):
        """
        It initializes a DataHandler object from a reports dataframe.

        Parameters
        ----------
        dataframe : a pandas.DataFrame object
            The dataframe containing the information from PELE reports

        Returns
        -------
        data_handler : a DataHandler object
            The DataHandler object obtained from the dataframe that was
            supplied
        """
        import os

        arbitrary_trajectory_path = list(dataframe['trajectory'])[0]

        sim_path = os.path.dirname(os.path.dirname(arbitrary_trajectory_path))
        report_name = None
        trajectory_name = os.path.basename(arbitrary_trajectory_path)

        columns = list(dataframe.columns)
        try:
            be_column = columns.index('Binding Energy') + 1
        except ValueError:
            be_column = None

        data_handler = DataHandler(sim_path, report_name, trajectory_name,
                                   be_column)
        data_handler._dataframe = dataframe

        return data_handler

    def get_reports_dataframe(self, from_scratch=False):
        """
        It returns the data stored in PELE reports as a pandas dataframe.

        Parameters
        ----------
        from_scratch : bool
            If it is set to True, a new dataframe will be generated from
            scratch. Default is False

        Returns
        -------
        dataframe : a pandas.DataFrame object
            The dataframe containing the information from PELE reports
        """
        # Return the dataframe if it has been already created,
        # unless a brand new dataset is requested
        if self._dataframe is not None and not from_scratch:
            return self._dataframe

        # This will happen when de DataHandler has been initialized from a
        # dataframe
        if self._report_name is None:
            raise Exception('Dataframe cannot be generated from scratch '
                            + 'when report names are unknown')

        import os
        import glob
        import pandas as pd
        from pele_platform.Utilities.Helpers import get_suffix

        # Initialize primary variables
        epoch_dirs = glob.glob(os.path.join(self._sim_path, '[0-9]*'))
        report_prefix = self._report_name
        trajectory_prefix = \
            str(os.path.splitext(self._trajectory_name)[0]) + '_'
        trajectory_format = \
            str(os.path.splitext(self._trajectory_name)[-1])

        # Filter out non digit folders
        epochs = [os.path.basename(path) for path in epoch_dirs
                  if os.path.basename(path).isdigit()]

        dataframe_lists = []
        for adaptive_epoch in sorted(epochs, key=int):
            folder = os.path.join(self._sim_path, str(adaptive_epoch))
            report_dirs = glob.glob(os.path.join(folder,
                                                 report_prefix + '_[0-9]*'))

            report_ids = [get_suffix(path) for path in report_dirs
                          if get_suffix(path).isdigit()]
            report_list = [os.path.join(folder, report_prefix + '_' + i)
                           for i in sorted(report_ids, key=int)]

            for i, report in enumerate(report_list, start=1):
                pandas_df = pd.read_csv(report, sep="    ", engine="python",
                                        index_col=False, header=0)
                pandas_df["epoch"] = adaptive_epoch
                pandas_df["trajectory"] = \
                    os.path.join(self._sim_path, adaptive_epoch,
                                 trajectory_prefix + str(i) +
                                 trajectory_format)
                dataframe_lists.append(pandas_df)

        self._dataframe = pd.concat(dataframe_lists, ignore_index=True)

        return self._dataframe

    def remove_outliers_from_dataframe(self, dataframe, threshold=None):
        """
        Given a dataframe, it removes the outliers by deleting the entries
        with highest values for the total and binding energy.

        Parameters
        ----------
        dataframe : a pandas.DataFrame object
            The dataframe containing the information from PELE reports
        threshold : float
            The ratio of high-energy entries that will be filtered out.
            Default is None and will be initialized with a threshold of
            0.02

        Returns
        -------
        dataframe : a pandas.DataFrame object
            The filtered dataframe containing the information from PELE
            reports
        """
        # Check threshold value
        if threshold is None:
            threshold = 0.02
        elif threshold >= 1 or threshold <= 0:
            raise ValueError('Invalid threshold value: '
                             'it must be higher than 0 and smaller than 1.')

        # Get the number of entries to remove
        cols = list(dataframe.columns)
        n_points_to_remove = int(len(dataframe[cols[0]]) * threshold)

        # Remove entries with higher total energies
        dataframe_filtered = dataframe.sort_values(
            cols[3], ascending=False).iloc[n_points_to_remove:]

        # Remove entries with higher interaction energies
        if self._be_column:
            dataframe_filtered = dataframe_filtered.sort_values(
                cols[self._be_column - 1],
                ascending=False).iloc[n_points_to_remove:]

        return dataframe_filtered

    def get_metrics(self):
        """
        It returns the labels that belong to the metrics in the dataframe.

        Returns
        -------
        metrics : list[str]
            The list of metrics that belong to the reports dataframe
        """
        # Get dataframe
        dataframe = self.get_reports_dataframe()

        # Get columns
        columns = set(dataframe.columns)

        # Filter out non metric columns
        metrics = list(columns.difference(self._NON_METRIC_LABELS))

        return metrics

    def get_number_of_metrics(self):
        """
        It returns the number of metrics in the dataset.

        Returns
        -------
        n_metrics : int
            The number of metrics in the dataset
        """
        # Get metrics
        metrics = self.get_metrics()

        # Calculate number of metrics
        n_metrics = len(metrics)

        return n_metrics

    def get_top_entries(self, metric, n_entries, criterion='lowest'):
        """
        It returns the top entries according to the supplied parameters.

        Parameters
        ----------
        metric : str
            The metric to evaluate
        n_entries : int
            The number of entries to return
        criterion : str
            The criterion to evaluate the metrics. One of ['lowest',
            'largest']. If 'lowest' the best entries will be those with
            the lowest values. If 'largest' the entries whose values are
            the largest will be retrieved. Default is 'lowest'

        Returns
        -------
        dataframe :  a pandas.DataFrame object
            The dataframe containing the top entries that were filtered
        """
        # Check metric value
        metrics = self.get_metrics()
        if not str(metric).isdigit() not in metrics:
            raise ValueError('Invalid metric: metric name not found '
                             + 'in the reports dataframe')

        # Ensure that metric is pointing to a dataframe column
        if str(metric).isdigit():
            metric = self._get_column_name(metric)

        # Check criterion value
        if criterion not in ['lowest', 'largest']:
            raise ValueError('Invalid criterion: it must be one of '
                             + '[\'smallest\', \'largest\']')

        if criterion == 'lowest':
            return self._dataframe.nsmallest(n_entries, metric)
        else:
            return self._dataframe.nlargest(n_entries, metric)

    def _get_column_name(self, column_index):
        """
        It returns the column name that corresponds to the index that is
        supplied. Take into account that the index starts at 1, not at 0.

        Parameters
        ----------
        column_index : int
            The index of the column whose name will be returned. It starts
            at 1, not at 0

        Returns
        -------
        column_name : str
            The name of the column that corresponds to the index that is
            supplied
        """
        dataframe = self.get_reports_dataframe()
        column_name = list(dataframe)[int(column_index) - 1]

        return column_name

    def extract_coords(self, residue_name, topology, remove_hydrogen=True):
        """
        This method employs mdtraj to extract the coordinates that
        belong to the supplied residue from all the trajectories in the
        dataframe. It supports both PDB and XTC trajectories.

        Parameters
        ----------
        residue_name : str
            A 3-char string that represent the residue that will be extracted
        topology : str
            Path to the PDB file representing the topology of the system.
        remove_hydrogen : bool
            Whether to remove all hydrogen atoms from the extracted
            coordinates array or not. Default is True

        Returns
        -------
        coordinates : numpy.array
            The array of coordinates that will be clustered. Its shape
            fulfills the following dimensions: [M, N, 3], where M is the
            total number of models that have been sampled with PELE and
            N is the total number of atoms belonging to the residue that
            is being analyzed
        dataframe :  a pandas.DataFrame object
            The dataframe containing the information from PELE reports
            that matches with the array of coordinates that has been
            extracted
        """
        import mdtraj
        import numpy as np
        import pandas as pd

        # Load topology
        topology = mdtraj.load(topology)

        # Select atom subset
        if remove_hydrogen:
            selection_str = \
                'resname == {} and symbol != H'.format(residue_name)
        else:
            selection_str = 'resname == {}'.format(residue_name)
        atom_indices = topology.top.select(selection_str)

        # Get trajectories from reports dataframe
        dataframe = self.get_reports_dataframe()

        reordered_dataframe = pd.DataFrame()
        trajectories = set(dataframe[self._TRAJECTORY_LABEL])

        coordinates = []
        for trajectory in trajectories:
            # Extract coordinates
            residue_frames = mdtraj.load(trajectory, top=topology,
                                         atom_indices=atom_indices)

            # Reorder entries in the dataset to match with the coordinate
            # ordering
            trajectory_rows = dataframe.query(
                'trajectory=="{}"'.format(trajectory))
            trajectory_rows = trajectory_rows.sort_values(['Step'],
                                                          ascending=True)

            # Remove first entry
            residue_frames = residue_frames[1:]
            trajectory_rows = trajectory_rows.query('Step!="0"')

            # Save extracted data
            coordinates.extend(residue_frames.xyz * 10)
            reordered_dataframe = \
                reordered_dataframe.append(trajectory_rows)

        coordinates = np.array(coordinates)

        return coordinates, reordered_dataframe

    def extract_raw_coords(self, residue_name, remove_hydrogen=True,
                           n_proc=1):
        """
        This method extracts the the coordinates that belong to the
        supplied residue from all the trajectories in the dataframe.
        The trajectories must be written as PDB files.

        Parameters
        ----------
        residue_name : str
            A 3-char string that represent the residue that will be extracted
        remove_hydrogen : bool
            Whether to remove all hydrogen atoms from the extracted
            coordinates array or not. Default is True
        n_proc : int
            The number of processors to employ to extract the coordinates.
            Default is 1, so the parallelization is deactivated

        Returns
        -------
        coordinates : numpy.array
            The array of coordinates that will be clustered. Its shape
            fulfills the following dimensions: [M, N, 3], where M is the
            total number of models that have been sampled with PELE and
            N is the total number of atoms belonging to the residue that
            is being analyzed
        dataframe :  a pandas.DataFrame object
            The dataframe containing the information from PELE reports
            that matches with the array of coordinates that has been
            extracted
        """
        import pandas as pd

        no_multiprocessing = False
        try:
            from multiprocessing import Pool
            from functools import partial
        except ImportError:
            no_multiprocessing = True
        import numpy as np

        dataframe = self.get_reports_dataframe()

        trajectories = list(set(dataframe[self._TRAJECTORY_LABEL]))

        if no_multiprocessing or n_proc == 1:
            coordinates = []
            for trajectory in trajectories:
                coordinates.append(
                    self._get_coordinates_from_trajectory(residue_name,
                                                          remove_hydrogen,
                                                          trajectory))
        else:
            parallel_function = partial(self._get_coordinates_from_trajectory,
                                        residue_name, remove_hydrogen)

            with Pool(n_proc) as pool:
                coordinates = pool.map(parallel_function, trajectories)

        coordinates = np.concatenate(coordinates)

        # Reorder entries in the dataset to match with the coordinate
        # ordering
        reordered_dataframe = pd.DataFrame()

        for trajectory in trajectories:
            # Retrieve entries belonging to this trajectory, sorted by step
            trajectory_rows = dataframe.query(
                'trajectory=="{}"'.format(trajectory))
            trajectory_rows = trajectory_rows.sort_values(['Step'],
                                                          ascending=True)

            # Remove first entry
            trajectory_rows = trajectory_rows.query('Step!="0"')

            # Append the resulting entries to the new reordered dataframe
            reordered_dataframe = \
                reordered_dataframe.append(trajectory_rows)

        return coordinates, reordered_dataframe

    def _get_coordinates_from_trajectory(self, residue_name, remove_hydrogen,
                                         trajectory):
        """
        Given the path of a trajectory, it returns the array of coordinates
        that belong to the chosen residue.

        The resulting array will have as many elements as models the
        trajectory has (excluding the first model which will be always
        skipped).

        This method is prone to be parallelized.

        .. todo ::
           * Output warnings with logger, not with print.

        Parameters
        ----------
        residue_name : str
            The name of the residue whose coordinates will be extracted
        remove_hydrogen : bool
            Whether to remove all hydrogen atoms from the extracted
            coordinates array or not. Default is True
        trajectory : str
            The trajectory to extract the coordinates from

        Returns
        -------
        coordinates : a numpy.Array object
            The resulting array of coordinates
        """
        import numpy as np
        coordinates = list()

        with open(trajectory) as f:
            inside_model = False
            current_model = 0

            for i, line in enumerate(f):
                if len(line) <= 6:
                    continue

                line_type = line[0:6]

                if line_type == "MODEL ":
                    if inside_model:
                        print('Warning: ENDMDL declaration for model ' +
                              '{} might be missing'.format(current_model))
                    inside_model = True
                    current_model += 1
                    model_coords = []

                if line_type == "ENDMDL":
                    if not inside_model:
                        print('Warning: MODEL declaration for model ' +
                              '{} might be missing'.format(current_model + 1))
                    inside_model = False
                    if len(model_coords) > 0:
                        coordinates.append(np.array(model_coords))

                # First model will always be skipped
                if current_model == 1:
                    continue

                if line_type == "ATOM  " or line_type == "HETATM":
                    current_residue_name = line[17:20]

                    if current_residue_name == residue_name:
                        # In case we have information about the element
                        # and we want to skip hydrogen atoms, do so
                        if remove_hydrogen and len(line) >= 78:
                            element = line[76:78]
                            element.strip()
                            if element == 'H':
                                continue

                        try:
                            x = float(line[30:38])
                            y = float(line[38:46])
                            z = float(line[46:54])
                        except ValueError:
                            print('Warning: invalid PDB format found in ' +
                                  'line {}'.format(i) +
                                  'of trajectory {}. '.format(trajectory) +
                                  'Its coordinates will be skipped.')

                        point = np.array((x, y, z))
                        model_coords.append(point)

        coordinates = np.array(coordinates)

        # When np.array.shape does not return a tuple of len 3 is because
        # its subarrays does not share the same dimensionality, so ligand
        # sizes are different.
        try:
            n_models_loaded, ligand_size, spatial_dimension = \
                coordinates.shape
        except ValueError:
            print('Warning: trajectory {} '.format(trajectory) +
                  'has an inconsistent ligand size throughout the models. ' +
                  'Its coordinates will be skipped.')

            # Return empty array
            return np.array(())

        if n_models_loaded != current_model - 1 or spatial_dimension != 3:
            print('Warning: unexpected dimensions found in the ' +
                  'coordinate array from trajectory {}. '.format(trajectory) +
                  'Its coordinates will be skipped.')

            # Return empty array
            return np.array(())

        return coordinates



