# Independent verification STOP — no repair/retry

```
Traceback (most recent call last):
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\G4C-E2-008\coordinator\independent_verifier.py", line 61, in <module>
    try:main()
        ~~~~^^
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\G4C-E2-008\coordinator\independent_verifier.py", line 32, in main
    centers=np.stack([x[s][y[s]==c].mean(0) for c in [1,2,3,4]]);raw=nearest(x[q],centers);diff=x[q,None,active]-centers[None,:,active];candidate=np.argmin(np.sum(diff*diff*weights,axis=2),axis=1)+1;active_ones=nearest(x[q][:,active],centers[:,active]);up=[]
                                                                                                ~^^^^^^^^^^^^^^^
IndexError: shape mismatch: indexing arrays could not be broadcast together with shapes (25972,) (59,) 

```
