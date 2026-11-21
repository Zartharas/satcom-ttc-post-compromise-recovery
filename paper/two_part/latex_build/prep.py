import re
s=open('/dev/stdin').read() if False else open('src.md',encoding='utf-8').read()
i=s.index('\n## 1. Introduction'); front,body=s[:i],s[i:]
open('front.md','w',encoding='utf-8').write(front)
body=body.replace('../figures_ieee/','figs/')
body=re.sub(r'!\[Figure \d+\. ','![',body)
open('body.md','w',encoding='utf-8').write(body)
