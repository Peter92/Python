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
