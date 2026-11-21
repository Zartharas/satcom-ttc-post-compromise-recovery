
import re,sys
s=open('main.tex',encoding='utf-8').read()
# 1. keep manuscript's literal section numbers; make headings unnumbered so class does not add A./1. on top
s=re.sub(r'\\(section|subsection|subsubsection|paragraph)\{',lambda m:'\\'+m.group(1)+'*{',s)
# 2. breakable monospace
def brk(m):
    t=m.group(1)
    t=t.replace('\\_','\\_\\allowbreak{}')
    t=re.sub(r'([A-Za-z0-9]{10})(?=[A-Za-z0-9])',r'\1\\allowbreak{}',t)
    return '\\texttt{'+t+'}'
s=re.sub(r'\\texttt\{((?:[^{}]|\\\{|\\\})*)\}',brk,s)
s=s.replace('\\usepackage{natbib}','\\usepackage{natbib}')
s=s.replace('\\begin{verbatim}','\\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\\scriptsize]').replace('\\end{verbatim}','\\end{Verbatim}')
s=s.replace('\\usepackage{graphicx','\\usepackage{fvextra}\n\\usepackage{graphicx',1)
s=s.replace('\\begin{document}','\\sloppy\n\\begin{document}',1)
open('main.tex','w',encoding='utf-8').write(s)

# ---- table post-processing ----
s=open('main.tex',encoding='utf-8').read()
def conv(m):
    blk=m.group(0)
    blk=blk.replace('\\_','\\_\\allowbreak{}')
    lines=blk.split('\n')
    head=[l for l in lines if l.startswith('\\begin{tabularx}')][0]
    n=head.count('raggedright')
    rows=[l.replace('\\hline','').rstrip()[:-2] for l in lines if '&' in l]
    cells=[[re.sub(r'\\allowbreak\{\}','',c).replace('\\_','_').replace('\\textbf{','').strip() for c in r.split(' & ')] for r in rows]
    minseg=[1]*n; mx=[1]*n
    for r in cells:
        for j,c in enumerate(r[:n]):
            segs=re.split(r'[ _\-/]',c)
            minseg[j]=max(minseg[j],max(len(x) for x in segs)+1)
            mx[j]=max(mx[j],len(c))
    w=[a+(0.15*b if n<8 else 0.0) for a,b in zip(minseg,mx)]; tot=sum(w); w=[x/tot for x in w]
    if n<8:
        spec=''.join('>{\\hsize=%.3f\\hsize\\raggedright\\arraybackslash}X'%(x*n) for x in w)
        return blk.replace(head,'\\begin{tabularx}{\\textwidth}{'+spec+'}',1)
    # wide table: multi-page longtable in a one-column block (a two-column float cannot break across pages)
    spec=''.join('>{\\raggedright\\arraybackslash}p{%.4f\\dimexpr\\textwidth-%d\\tabcolsep\\relax}'%(x,2*n) for x in w)
    cap=re.search(r'\\caption\{(.*?)\}\n\\label',blk,re.S).group(1)
    lab=re.search(r'\\label\{([^}]*)\}',blk).group(1)
    body=[l for l in lines if '&' in l]
    hdr=body[0]; rest=body[1:]
    out=['\\clearpage\\onecolumn','{\\scriptsize\\setlength{\\tabcolsep}{2pt}',
         '\\begin{longtable}{'+spec+'}',
         '\\caption{'+cap+'}\\label{'+lab+'}\\\\','\\hline',hdr.rstrip(),'\\endfirsthead',
         '\\hline',hdr.rstrip(),'\\endhead','\\hline\\endfoot']
    out+=rest
    out+=['\\hline','\\end{longtable}','}','\\clearpage\\twocolumn']
    return '\n'.join(out)
s=re.sub(r'\\begin\{table\*\}.*?\\end\{table\*\}',conv,s,flags=re.S)
s=s.replace('\\usepackage{fvextra}','\\usepackage{fvextra}\n\\usepackage{longtable}',1)
open('main.tex','w',encoding='utf-8').write(s)
s=open('main.tex',encoding='utf-8').read()
m=re.search(r'\\clearpage\\onecolumn.*?\\clearpage\\twocolumn',s,flags=re.S)
if m:  # only when a wide table is still in the main text (not in --compact output)
    blk=m.group(0)
    s=s.replace(blk,'',1)
    s=s.replace('\\bibliographystyle{IEEEtaes}',blk+'\n\\bibliographystyle{IEEEtaes}',1)
    open('main.tex','w',encoding='utf-8').write(s)
