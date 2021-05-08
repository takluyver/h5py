#!/usr/bin/python
"""Error copying (unable to insert object) after repeated copy & delete

https://github.com/h5py/h5py/issues/1886
"""

import h5py
import numpy as np

def main():
    ft = h5py.File('test.hdf5','w')

    h5py._errors.unsilence_errors()

    # Create the 1st event
    grp = ft.create_group("Event_1")
    # Some random, copied dataset
    grp.create_dataset("ds", data=np.random.rand(40).astype(dtype=np.float32))
    # Create traces in the first group
    trace_length = 1000
    for k in range(200):
        x1 = np.random.rand(trace_length).astype(dtype=np.float32)

        grp = ft.create_group(f"/Event_1/Traces_A{k}")
        grp.create_dataset("SimEfield_X", data=x1)

    # Create 100 more events, through copying, deleting, overwriting
    for ev in range(100):
        print(f"Event_{ev+2}", ev+2)
        # Copy the event
        ft.copy(ft["Event_1"], ft["/"], name="Event_%d"%(ev+2))

        print(ft["Event_1/Traces_A199"])

        # Delete the traces copied from Event_1
        for trr in range(200):
            print(f"/Event_{ev+2}/Traces_A{trr}")
            del ft[f"/Event_{ev+2}/Traces_A{trr}"]

    return ft

if __name__ == '__main__':
    try:
        a = main()
    except Exception:
        input()
