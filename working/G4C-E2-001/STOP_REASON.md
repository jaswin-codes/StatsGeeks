# STOP — entire G4C suite

No retry or repair authorized.

```
Traceback (most recent call last):
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\run_g4c_candidate.py", line 33, in main
    inputs=integrity();m=json.loads((ROOT/'working/gate4_episode_manifest.json').read_text());assert m['gate4a']=='PASS' and len(m['episodes'])==60
           ^^^^^^^^^^^
  File "C:\Users\jaswi\Downloads\Hackathon3_StatsGeeks - Copy\working\run_g4c_candidate.py", line 19, in integrity
    assert not failures,('Pre-existing input/code/evidence mutation',failures)
           ^^^^^^^^^^^^
AssertionError: ('Pre-existing input/code/evidence mutation', ['working/Open Notebook.onetoc2'])

```
