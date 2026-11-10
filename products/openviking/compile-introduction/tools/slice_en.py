import json,subprocess,wave
L=json.load(open('lines.json'));Ld=dict(L);P=json.load(open('paras.json'))
out={}
for pid,ids in P:
  W=json.load(open(f'raw/{pid}.wav.json'))
  n=wave.open(f'raw/{pid}.wav').getnframes()/24000
  k=0;groups=[]
  for i in ids:
    c=len(Ld[i].split()); groups.append(W[k:k+c]); k+=c
  assert k==len(W),(pid,k,len(W))
  for j,(i,g) in enumerate(zip(ids,groups)):
    a=0 if j==0 else (groups[j-1][-1]['endTime']+g[0]['startTime'])/2
    b=n if j==len(ids)-1 else (g[-1]['endTime']+groups[j+1][0]['startTime'])/2
    if j==0: a=max(0,g[0]['startTime']-0.12)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'raw/{pid}.wav','-ss',f'{a:.3f}','-to',f'{b:.3f}','-af','afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse',f'cut/{i}.wav'])
    out[i]={'dur':round(b-a,3),'words':[{'w':x['word'],'s':round(x['startTime']-a,3),'e':round(x['endTime']-a,3)} for x in g]}
json.dump(out,open('words.json','w'),indent=1)
for i in out: print(i,out[i]['dur'],out[i]['words'][0]['s'],out[i]['words'][-1]['e'])
