"""Assemble authored study material; does not execute or import any ML implementation."""
from pathlib import Path
import sys,json,collections
T=Path(__file__).resolve().parent;sys.path.insert(0,str(T))
from question_bank import QUESTIONS

def main():
    assert len(QUESTIONS)==66
    counts=collections.Counter(q[0] for q in QUESTIONS);assert len(counts)==22 and set(counts.values())=={3}
    source=(T/'PROJECT_NARRATIVE.md').read_text(encoding='utf-8');assert source.count('<!-- QUESTION_BANK_INSERTION -->')==1
    lines=[];previous=None;bank=[]
    for i,(group,q,short,deep,facts,trap) in enumerate(QUESTIONS,1):
        if group!=previous:lines.extend(['### '+group,'']);previous=group
        lines.extend([f'#### Q{i:02d}',f'**QUESTION:** {q}',f'**SHORT ANSWER:** {short}',f'**DEEPER ANSWER:** {deep}',f'**KEY NUMBERS/FACTS:** {facts}',f'**COMMON MISTAKE TO AVOID:** {trap}',''])
        bank.append(dict(id=f'Q{i:02d}',category=group,question=q,short_answer=short,deeper_answer=deep,key_numbers_facts=facts,common_mistake_to_avoid=trap))
    out=T/'PROJECT_MASTER_GUIDE.md';assert not out.exists(),'Do not overwrite an existing study edition without review'
    out.write_text(source.replace('<!-- QUESTION_BANK_INSERTION -->','\n'.join(lines)),encoding='utf-8')
    (T/'QUESTION_BANK.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Master guide:',len(out.read_text(encoding='utf-8').split()),'words;',len(bank),'questions in',len(counts),'categories')
if __name__=='__main__':main()
