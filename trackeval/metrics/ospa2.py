import numpy as np
from scipy.optimize import linear_sum_assignment
from ._base_metric import _BaseMetric
from .. import _timing
from .. import utils


class OSPATrack(_BaseMetric):
    """Class which implements the OSPA(2) metric"""

    @staticmethod
    def get_default_config():
        """Default class config values"""
        default_config = {
            'PRINT_CONFIG': True,  # Whether to print the config information on init. Default: False.
        }
        return default_config

    def __init__(self, config=None):
        super().__init__()
        self.float_fields = ['OSPA2', 'OSPA2_CARD', 'OSPA2_LOC']
        self.fields = self.float_fields
        self.summary_fields = self.fields

        # Configuration options:
        self.config = utils.init_config(config, self.get_default_config(), self.get_name())

    @_timing.time
    def eval_sequence(self, data):
        """Calculates OSPA(2) metric for one sequence"""

        # Initialise results
        res = {}
        for field in self.fields:
            res[field] = 0
        c, p = 1, 1     # Fix cut-off and p-order
        all_gt_ids = np.concatenate(data['gt_ids'])
        unique_gt_ids = np.unique(all_gt_ids)

        all_tracker_ids = np.concatenate(data['tracker_ids'])
        unique_tracker_ids = np.unique(all_tracker_ids)

        m, n = len(unique_gt_ids), len(unique_tracker_ids)

        if m == 0 or n == 0:
            res['OSPA2_CARD'] = c if m != n else 0
            res['OSPA2_LOC'] = 0
            res['OSPA2'] = c if m != n else 0
            return res

        # Precompute concatenated IDs and time blocks for both GT and tracker data
        gt_ids = np.concatenate(data['gt_ids'])
        tracker_ids = np.concatenate(data['tracker_ids'])

        # Vectorize the creation of time blocks and index blocks
        num_timesteps = data['num_timesteps']
        timeblock_gt = np.repeat(np.arange(num_timesteps), [len(ids) for ids in data['gt_ids']])
        idxblock_gt = np.concatenate([np.arange(len(ids)) for ids in data['gt_ids']])

        timeblock_tracker = np.repeat(np.arange(num_timesteps), [len(ids) for ids in data['tracker_ids']])
        idxblock_tracker = np.concatenate([np.arange(len(ids)) for ids in data['tracker_ids']])

        # Initialize the all_trk_dist array
        all_trk_dist = np.full((m, n, num_timesteps), np.nan, dtype=float)

        # Loop through each unique GT and tracker ID pair
        for ii, gt_id in enumerate(unique_gt_ids):
            for jj, tracker_id in enumerate(unique_tracker_ids):
                # Find indices of the current GT and tracker IDs in the concatenated arrays
                gt_idx_in_concat = np.where(gt_ids == gt_id)[0]
                tracker_idx_in_concat = np.where(tracker_ids == tracker_id)[0]

                # Extract the corresponding time and original index blocks
                gt_time, gt_ori_idx = timeblock_gt[gt_idx_in_concat], idxblock_gt[gt_idx_in_concat]
                tracker_time, tracker_ori_idx = timeblock_tracker[tracker_idx_in_concat], idxblock_tracker[
                    tracker_idx_in_concat]

                # Find common times between GT and tracker
                common_time = np.intersect1d(gt_time, tracker_time)
                tmp_gt_indices = gt_ori_idx[np.in1d(gt_time, common_time)]
                tmp_tracker_indices = tracker_ori_idx[np.in1d(tracker_time, common_time)]

                # Set distances to c for all times in gt_time and tracker_time
                all_trk_dist[ii, jj, gt_time] = c
                all_trk_dist[ii, jj, tracker_time] = c

                # Update distances based on similarity scores for common times
                for common_idx, time in enumerate(common_time):
                    gt_idx_time = tmp_gt_indices[common_idx]
                    tracker_idx_time = tmp_tracker_indices[common_idx]
                    all_trk_dist[ii, jj, time] = 1 - data['similarity_scores'][time][gt_idx_time, tracker_idx_time]

        # Compute the mean distance across all timesteps
        all_trk_dist = np.clip(all_trk_dist, None, c)  # Cut-off threshold
        trk_dist = np.nanmean(all_trk_dist, axis=2)
        trk_dist = np.power(trk_dist, p)
        match_rows, match_cols = linear_sum_assignment(trk_dist)
        cost = trk_dist[match_rows, match_cols].sum()

        # Get the distance
        res['OSPA2_CARD'] = (((c ** p * abs(m - n)) / max(m, n)) ** (1 / p)) / c
        res['OSPA2_LOC'] = (cost / max(m, n)) ** (1 / p) / c
        res['OSPA2'] = ((c ** p * abs(m - n) + cost) / max(m, n)) ** (1 / p) / c
        return res

    def combine_classes_class_averaged(self, all_res, ignore_empty_classes=False):
        """Combines metrics across all classes by averaging over the class values.
        'ignore_empty_classes' is dummy here. If both prediction and ground truth are empty, the cost is 0 anyway.
        """
        res = {}
        for field in self.float_fields:
            res[field] = np.mean([v[field] for v in all_res.values()], axis=0)
        return res

    def combine_classes_det_averaged(self, all_res):
        """Combines metrics across all classes by averaging over the detection values"""
        res = {}
        for field in self.float_fields:
            res[field] = np.mean([v[field] for v in all_res.values()], axis=0)
        return res

    def combine_sequences(self, all_res):
        """Combines metrics across all sequences"""
        res = {}
        for field in self.float_fields:
            res[field] = np.mean([v[field] for v in all_res.values()], axis=0)
        return res

    @staticmethod
    def _compute_final_fields(res):
        """Calculate sub-metric ('field') values which only depend on other sub-metric values.
        This function is used both for both per-sequence calculation, and in combining values across sequences.
        """
        return res
