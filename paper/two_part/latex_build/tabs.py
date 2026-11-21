import re,subprocess,sys,functools
@functools.lru_cache(None)
def tex(s):
    s=s.strip()
    if not s: return ''
    r=subprocess.run(['pandoc','-f','markdown','-t','latex','--wrap=none'],input=s,capture_output=True,text=True,check=True)
    return r.stdout.strip().replace('\n\n',' ')
def split(line):
    line=line.strip()
    if line.startswith('|'): line=line[1:]
    if line.endswith('|'): line=line[:-1]
    # split on unescaped pipes
    return [c for c in re.split(r'(?<!\\)\|',line)]
lines=open(sys.argv[1],encoding='utf-8').read().split('\n')
out=[];i=0
while i<len(lines):
    m=re.match(r'^\*\*Table (\d+)\.\s*(.*)\*\*\s*$',lines[i])
    j=i+1
    while m and j<len(lines) and lines[j].strip()=='' : j+=1
    if m and j<len(lines) and lines[j].startswith('|'):
        num,cap=m.group(1),m.group(2)
        k=j; rows=[]
        while k<len(lines) and lines[k].startswith('|'):
            rows.append(lines[k]); k+=1
        hdr=split(rows[0]); body=[split(r) for r in rows[2:]]
        n=len(hdr)
        L=['```{=latex}','\\begin{table*}[!t]','\\caption{'+tex(cap)+'}','\\label{tab:'+num+'}','\\footnotesize','\\setlength{\\tabcolsep}{3pt}',
           '\\begin{tabularx}{\\textwidth}{'+'>{\\raggedright\\arraybackslash}X'*n+'}','\\hline',
           ' & '.join('\\textbf{'+tex(c)+'}' for c in hdr)+' \\\\ \\hline']
        for r in body:
            r=(r+['']*n)[:n]
            L.append(' & '.join(tex(c) for c in r)+' \\\\')
        L+=['\\hline','\\end{tabularx}','\\end{table*}','```']
        out+=L; i=k
    else:
        out.append(lines[i]); i+=1
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
