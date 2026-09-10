"""Test the exported ZIP in an isolated temporary directory; no optimization."""
from pathlib import Path
import tempfile,zipfile,subprocess,sys,json,hashlib
R=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    logs=[]
    with tempfile.TemporaryDirectory(prefix='statsgeeks_publication_') as temp:
        root=Path(temp)
        with zipfile.ZipFile(R/'candidate/publication/submission_bundle.zip') as z:z.extractall(root)
        for args in [['-B','candidate/publication/validate_package.py'],['-I','-B','reproduce_best.py','--verify','--out','isolated_replay'],['-B','candidate/publication/build_publication.py']]:
            result=subprocess.run([sys.executable,*args],cwd=root,text=True,capture_output=True)
            logs.append(dict(command='python '+' '.join(args),returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
            assert result.returncode==0,logs[-1]
        comparisons={p.name:sha(p)==sha(root/'candidate/tables'/p.name) for p in (R/'candidate/tables').glob('*.csv')}
        assert all(comparisons.values()),comparisons
        metadata=json.loads((root/'isolated_replay/metadata.json').read_text())
    output=dict(passed=True,archive_sha256=sha(R/'candidate/publication/submission_bundle.zip'),extracted_outside_repository=True,original_repository_dependencies_used=False,git_directory_absent=True,packaged_coordinate_reference_arrays=metadata['exact_verification_arrays'],all_rebuilt_csv_byte_identical=all(comparisons.values()),csv_comparisons=comparisons,commands=logs,scope='archive integrity plus five inference references plus complete evidence-only rebuild; no source refit or optimization')
    (R/'candidate/publication/distribution_test_receipt.json').write_text(json.dumps(output,indent=2))
    print(json.dumps({k:v for k,v in output.items() if k not in ('commands','csv_comparisons')},indent=2))
if __name__=='__main__':main()
