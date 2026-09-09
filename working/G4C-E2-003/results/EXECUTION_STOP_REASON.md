# E2 execution STOP — no retry

```
Traceback (most recent call last):
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\G4C-E2-003\coordinator\execution_coordinator.py", line 121, in <module>
    try:main()
        ^^^^^^
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\G4C-E2-003\coordinator\execution_coordinator.py", line 74, in main
    with open(ROOT/'data/preprocessed/preprocessed_data.pkl','rb') as f:d=pickle.load(f)
                                                                          ^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'working'

```
