import re,subprocess
f=open('front.md',encoding='utf-8').read()
m=re.search(r'## Abstract\s+(.*?)\n\*\*Keywords:\*\*\s*(.*?)\n',f,re.S)
abstract=m.group(1).strip(); kw=m.group(2).strip().rstrip('.')
def tx(s): return subprocess.run(['pandoc','-f','markdown','-t','latex','--wrap=none'],input=s,capture_output=True,text=True).stdout.strip()
title=re.search(r'^# (.*)$',f,re.M).group(1)
body=open('body.tex',encoding='utf-8').read()
# fig3 is a one-column figure; fig1/fig2 are page-wide
parts=re.split(r'(\\begin\{figure\}.*?\\end\{figure\})',body,flags=re.S); out=[]
for p in parts:
    if p.startswith('\\begin{figure}'):
        if 'fig3' in p:
            p=p.replace('\\begin{figure}','\\begin{figure}[!t]').replace('\\includegraphics{','\\includegraphics[width=\\columnwidth]{')
        else:
            p=p.replace('\\begin{figure}','\\begin{figure*}[!t]').replace('\\end{figure}','\\end{figure*}').replace('\\includegraphics{','\\includegraphics[width=0.9\\textwidth]{')
    out.append(p)
body=''.join(out)
tex=r'''\documentclass{IEEEtaes}
\usepackage{color,array,amsthm,amsmath,amssymb}
\usepackage{graphicx,booktabs,tabularx,url,xcolor}
\usepackage[numbers,sort&compress]{natbib}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\jvol{XX}\jnum{XX}\jmonth{XXXXX}\paper{0000000}\pubyear{2026}\doiinfo{TAES.2026.Doi Number}
\setcounter{page}{1}
\begin{document}
\title{'''+tx(title)+r'''}
\author{AUTHOR NAME PLACEHOLDER -- HOLD}
\affil{AFFILIATION PLACEHOLDER -- author-confirmed value required}
\markboth{AUTHOR ET AL.}{POST-COMPROMISE RESYNCHRONIZATION UNDER INTERMITTENT LINKS}
\maketitle
\begin{abstract}'''+tx(abstract)+r'''\end{abstract}
\begin{IEEEkeywords}'''+tx(kw)+r'''\end{IEEEkeywords}
'''+body+r'''
\bibliographystyle{IEEEtaes}
\bibliography{bibliography}
\end{document}
'''
open('main.tex','w',encoding='utf-8').write(tex)
