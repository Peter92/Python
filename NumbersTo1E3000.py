num_units = ['zero','one','two','three','four','five','six','seven','eight','nine']
num_teens = ['ten','eleven','twelve']+[i+('t' if i[-1]!='t' else '')+'een' for i in ['thir','four','fif']+num_units[6:]]
num_tens = [i+('ty' if i[-1]!='t' else 'y') for i in ['twen','thir','for','fif']+num_units[6:]]
num_exp_prefix = ['', 'un','duo','tre','quattor','quin','sex','septen','octo','novem']
num_exp_amount = ['']+[i+'int' for i in ['vig','trig','quadrag','quinquag','sexag','septuag','octog','nonag']]
num_exp_units = [i+'illion' for i in ['m','b','tr','quadr','quint','sext','sept','oct','non']]
num_exp_tens = [j+'illion' for j in ['dec']+num_exp_amount[1:]]
num_exp_hundreds = ['']+[i+'en' for i in ['c','duoc','trec','quadring','quing','sesc','septing','octing','nong']]
num_list = ['thousand']+num_exp_units
for i in num_exp_hundreds:
    num_list2 += [i+j+k for k in num_exp_tens for j in num_exp_prefix]
    if not i: num_exp_tens = ['tillion']+num_exp_tens


#short version
a=[''];m,n,o,p,q,r,s,t,u,v,w,x,y,z='illion quadr quin sex sept oct non ing ag g tre duo c t'.split();l=['thousand']+[i+m for i in['m','b','tr',n,o+z,p+z,q,r,s]]+[i+j+k for i in a+[i+'en'for i in[y,x+y,w+y,n+t,o+v,'sesc',q+t,r+t,s+v]] for k in [C+m for C in['t','dec']+[B+'int'for B in['vig','trig',n+u,o+'quag',p+u,q+'uag',r+v,s+u]]][not i:]for j in a+['un',x,w,'quattor',o,p,q+'ten',r+'o','novem']]



X='-1'+'9'*5010
m,n,o,p,q,r,s,t,u,v,w,x,y,z='illion quadr quin sex sept oct non ing ag g tre duo c t'.split();a=[''];l=a+['thousand']+[i+m for i in['m','b','tr',n,o+z,p+z,q,r,s]]+[i+j+k for i in a+[i+'en'for i in[y,x+y,w+y,n+t,o+v,'sesc',q+t,r+t,s+v]]for k in[C+m for C in['t','dec']+[B+'int'for B in['vig','trig',n+u,o+'quag',p+u,q+'uag',r+'og',s+u]]][not i:]for j in a+['un',x,w,'quattor',o,p,q+'en',r+'o','novem']];N=str(X).split('.');E=min(1000,(len(N[0].replace('-',''))-1)/3);P=N[0][:(-E*3 if E else len(N[0]))];B=''.join(N);L=len(P);O=round(float((P+'.'+((B[L:L+2])or'0'))));print O,l[E]
