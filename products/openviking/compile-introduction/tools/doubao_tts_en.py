import sys, json, uuid, base64, wave, urllib.request
key=json.load(open('/home/zhiheng.liu/.config/doubao-tts/credentials.json'))['api_key']
speaker,res,out,text=sys.argv[1:5]
hdr={'X-Api-Key':key,'X-Api-Resource-Id':res,'X-Api-Request-Id':str(uuid.uuid4()),'Content-Type':'application/json','User-Agent':'curl/8.0'}
body={'req_params':{'text':text,'speaker':speaker,'audio_params':{'format':'pcm','sample_rate':24000,'enable_timestamp':True,'enable_subtitle':True},
 'additions':json.dumps({'enable_timestamp':True,'enable_subtitle':True})}}
req=urllib.request.Request('https://openspeech.bytedance.com/api/v3/tts/unidirectional',data=json.dumps(body).encode(),headers=hdr)
pcm=b'';words=[]
try:
  with urllib.request.urlopen(req,timeout=60) as r:
    for line in r:
      if not line.strip(): continue
      ev=json.loads(line); c=ev.get('code',0)
      if c not in (0,20000000): print('REJ',c,ev.get('message','')[:150]); sys.exit(2)
      if ev.get('data'): pcm+=base64.b64decode(ev['data'])
      if ev.get('sentence'): words+=ev['sentence'].get('words',[]) if isinstance(ev['sentence'],dict) else []; 
      for k in ev:
        if k not in('data','code','message'): print('EV',k,str(ev[k])[:300])
except urllib.error.HTTPError as e: print('HTTP',e.code,e.read()[:200]); sys.exit(3)
w=wave.open(out,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(pcm[:len(pcm)//2*2])
json.dump(words,open(out+'.json','w'))
print('ok',len(pcm)/48000,len(words))
