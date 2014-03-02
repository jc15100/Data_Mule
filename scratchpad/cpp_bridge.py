#!/usr/bin/env python

# Call with 'cpp_bridge.py pickle_filename id1 id2'

__author__ = 'arprice'

import sys
import os.path
import cPickle as pickle


if __name__ == "__main__":
    filename = sys.argv[1]

    pending_data = set()
    completed_ids = set()
    
    if not os.path.isfile(filename):
        with open(filename, "wb+") as f:
            pickle.dump((pending_data, completed_ids), f)

    with open(filename, "rb+") as f:
        # Load the existing data
        try:
            pending_data, completed_ids = pickle.load(f)
        except EOFError:
            # Do nothing
            print "File doesn't exist yet."

        print pending_data

        # Add in the new data IDs
        for i, arg in enumerate(sys.argv):
            if i > 1:
                pending_data.add(arg)

        print pending_data

        # Save the data to the file store
        f.seek(0)
        pickle.dump((pending_data, completed_ids), f)
