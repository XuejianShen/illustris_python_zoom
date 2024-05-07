from __future__ import print_function

import numpy as np
import six
from os.path import isfile

# --------------------------------------------------------------------------------------------------
# center position, velocity
# --------------------------------------------------------------------------------------------------
# an iterative method to find the center of a distribution of particles developed by Andrew Wetzel
def get_center_position(
    positions,
    weights=None,
    position_number_min=32,
    center_position_initial=None,
    distance_max=np.inf,
    ):
    
    distance_bins = np.append(np.inf, np.logspace(4, -3, 201))
    '''
    distance_bins = np.array([np.inf, 
            10000, 7000, 5000, 3000, 2000, 1500, 1000,
            700, 500, 300, 200, 150, 100,
            70, 50, 30, 20, 15, 10, 
            7, 5, 3, 2, 1.5, 1,
            0.7, 0.5, 0.3, 0.2, 0.15, 0.1,
            0.07, 0.05, 0.03, 0.02, 0.015, 0.01,
            0.007, 0.005, 0.003, 0.002, 0.0015, 0.001,
        ]
    )
    '''

    distance_bins = distance_bins[distance_bins <= distance_max]
    # fix weights
    if weights is not None:
        assert positions.shape[0] == weights.size
        # normalize weights by median, improves numerical stability
        weights = weights / np.median(weights)

    # initialize center position
    if center_position_initial is None:
        center_position = np.zeros(positions.shape[1], positions.dtype)
    else:
        center_position = np.array(center_position_initial, positions.dtype)

    idtype = np.int64 if positions.shape[0] > 2147483647 else np.int32
    part_indices = np.arange(positions.shape[0], dtype=idtype)
    for dist_i, dist_max in enumerate(distance_bins):
        part_distances = np.linalg.norm( positions[part_indices] - center_position, axis=1) 
        # get particles within distance max
        masks = part_distances < dist_max
        part_indices_dist = part_indices[masks]

        # store particles slightly beyond distance max for next interation
        masks = part_distances < dist_max * 1.5
        part_indices = part_indices[masks]

        # check whether reached minimum total number of particles within distance
        # but force at least one loop over distance bins to get *a* center
        if part_indices_dist.size <= position_number_min and dist_i > 0:
            return center_position
        
        if weights is None:
            weights_use = weights
        else:
            weights_use = weights[part_indices_dist]

        # ensure that np.average uses 64-bit internally for accuracy, but returns as input dtype
        #print(len(positions[part_indices_dist]))
        center_position = np.average(positions[part_indices_dist].astype(np.float64), 
                                     axis=0, 
                                     weights = weights_use
                                    ).astype(positions.dtype)
    return center_position


def get_center_velocity(
    velocities,
    weights=None,
    positions=None,
    center_position=None,
    distance_max=10
):
    masks = np.full(velocities.shape[0], True)
    # ensure that use only finite values of velocities
    for dimen_i in range(velocities.shape[1]):
        masks *= np.isfinite(velocities[:, dimen_i])

    if (positions is not None) and (center_position is not None) and (len(center_position) > 0):
        assert velocities.shape == positions.shape
        distances = np.linalg.norm( positions - center_position, axis=1)
        masks *= distances < distance_max

    if weights is not None:
        assert velocities.shape[0] == weights.size
        # normalizing weights by median seems to improve numerical stability
        weights = weights[masks] / np.median(weights[masks])

    if not masks.any():
        print('!cannot compute host/center velocity')
        print('no positions within distance_max = {:.3f} kpc comoving'.format(distance_max))
        print('nearest = {:.3f} kpc comoving'.format(np.sqrt(distances.min())))
        return np.r_[np.nan, np.nan, np.nan]

    # ensure that np.average uses 64-bit internally for accuracy, but returns as input dtype
    return np.average(velocities[masks].astype(np.float64), 0, weights).astype(velocities.dtype)


def get_stellar_prop_iterative(
    positions,
    masses,
    center_position=None,
    distance_max=10
    ):
    pass 