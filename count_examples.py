"""Find number of examples in MNE-Python.
"""

# Author: Mainak Jas <mainak.jas@telecom-paristech.fr>

import os
import os.path as op
import fnmatch

from mne.datasets import sample


def recursive_search(path, pattern):
    """Auxiliary function for recursive_search of the directory.
    """
    filtered_files = list()
    for dirpath, dirnames, files in os.walk(path):
        for f in fnmatch.filter(files, pattern):
            filtered_files.append(op.realpath(op.join(dirpath, f)))

    return filtered_files

# assuming sample data is in examples dir
example_path = op.dirname(sample.data_path())
tutorial_path = op.join(op.split(example_path)[0], 'tutorials')
tutorial_files = recursive_search(tutorial_path, '*.py')
example_files = recursive_search(example_path, '*.py')
print('Number of examples is %d' % len(example_files))
print('Number of tutorials is %d' % len(tutorial_files))
