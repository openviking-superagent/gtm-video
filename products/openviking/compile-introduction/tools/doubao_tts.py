"""Doubao seed-tts (v3 unidirectional HTTP) -> 24 kHz mono WAV. Auth/body mirror zoom-ov-bridge ovbridge/colleague/doubao.py.
usage: doubao_tts.py ENVFILE SPEAKER OUT.wav TEXT [speech_rate]"""
import sys, json, uuid, base64, wave, urllib.request
envf, speaker, out, text = sys.argv[1:5]
rate = int(sys.argv[5]) if len(sys.argv) > 5 else 0
env = {}
for l in open(envf):
    l = l.strip()
    if l and not l.startswith('#') and '=' in l:
        k, v = l.split('=', 1); env[k.strip()] = v.strip().strip('"').strip("'")
key = env.get('DOUBAO_TTS_API_KEY') or env.get('DOUBAO_AUDIO') or env.get('DOUBAO_API_KEY')
hdr = {'X-Api-Key': key, 'X-Api-Resource-Id': env.get('DOUBAO_TTS_RESOURCE') or 'seed-tts-2.0',
       'X-Api-Request-Id': str(uuid.uuid4()), 'X-Api-Connect-Id': str(uuid.uuid4()),
       'Content-Type': 'application/json', 'User-Agent': 'curl/8.0'}
body = {'req_params': {'text': text, 'speaker': speaker,
        'audio_params': {'format': 'pcm', 'sample_rate': 24000, 'speech_rate': rate}}}
req = urllib.request.Request('https://openspeech.bytedance.com/api/v3/tts/unidirectional', data=json.dumps(body).encode(), headers=hdr)
pcm = b''
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        for line in r:
            if not line.strip(): continue
            ev = json.loads(line); code = ev.get('code', 0)
            if code not in (0, 20000000):
                print(f'REJECT code={code} msg={str(ev.get("message",""))[:120]}'); sys.exit(2)
            if ev.get('data'): pcm += base64.b64decode(ev['data'])
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code} {e.read()[:160]!r}'); sys.exit(3)
if not pcm: print('EMPTY'); sys.exit(4)
with wave.open(out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm[:len(pcm)//2*2])
print(f'ok {out} {len(pcm)/48000:.2f}s')
