import numpy as np
from scipy.optimize import linear_sum_assignment
from ._base_metric import _BaseMetric
from .. import _timing
from .. import utils


class OSPADetection(_BaseMetric):
    """Class which implements the OSPA metric"""

    @staticmethod
    def get_default_config():
        """Default class config values"""
        default_config = {
            'PRINT_CONFIG': True,  # Whether to print the config information on init. Default: False.
        }
        return default_config

    def __init__(self, config=None):
        super().__init__()
        self.float_fields = ['OSPA', 'OSPA_CARD', 'OSPA_LOC']
        self.fields = self.float_fields
        self.summary_fields = self.fields

        # Configuration options:
        self.config = utils.init_config(config, self.get_default_config(), self.get_name())

    @_timing.time
    def eval_sequence(self, data):
        # Initialise results
        res = {}
        for field in self.fields:
            res[field] = 0
        # Default values
        c, p = 1, 1  # Fix cut-off and p-order
        """Calculates OSPA metric for one sequence"""
        all_ospa = np.full((3, data['num_timesteps']), c, dtype=float)
        for kk in range(data['num_timesteps']):
            m = len(data['gt_ids'][kk])
            n = len(data['tracker_ids'][kk])
            if m == 0 or n == 0:
                all_ospa[0, kk] = c if m != n else 0
                all_ospa[1, kk] = 0
                all_ospa[2, kk] = c if m != n else 0
                continue
            match_rows, match_cols = linear_sum_assignment(data['similarity_scores'][kk])
            cost = data['similarity_scores'][kk][match_rows, match_cols].sum()
            all_ospa[0, kk] = ((c ** p * abs(m - n) + cost) / max(m, n)) ** (1 / p) / c # OSPA
            all_ospa[1, kk] = (((c ** p * abs(m - n)) / max(m, n)) ** (1 / p)) / c # OSPA_CARD
            all_ospa[2, kk] = (cost / max(m, n)) ** (1 / p) / c # OSPA_LOC
        res['OSPA'] = np.mean(all_ospa[0])
        res['OSPA_CARD'] = np.mean(all_ospa[1])
        res['OSPA_LOC'] = np.mean(all_ospa[2])
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
