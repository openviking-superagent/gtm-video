import re,json
G=[(2.95,1.2),(14.9,0.7),(27.3,0.5),(29.9,0.7),(39.2,0.55),(41.9,0.85),(60.0,0.7)]
W=lambda t: round(t+sum(d for g,d in G if t>=g-1e-6),3)
comp={'hook':(0,[]),'console':(7.9,[]),'outputs':(47.3,[]),'endcard':(60.9,[])}
for name,(st,L) in comp.items():
    nxt={'hook':8.3,'console':47.9,'outputs':61.3,'endcard':67.9}[name]
    for g,d in G:
        if st<=g<nxt: L.append((round(g-st,3),d))
for name,(st,L) in comp.items():
    if not L: continue
    p=f'project-en/compositions/{name}.html'; s=open(p).read()
    code=f'''      // English narration runs longer: extra holds in local seconds (all children at/after a point shift later)
      const EN_HOLDS = {json.dumps(L)};
      const EW = (t) => EN_HOLDS.reduce((a, h) => a + (t >= h[0] - 1e-6 ? h[1] : 0), t);
      tl.getChildren(false, true, true).forEach((c) => c.startTime(EW(c.startTime())));
      window.__timelines["{name}"] = tl;'''
    s=s.replace(f'      window.__timelines["{name}"] = tl;',code,1); open(p,'w').write(s)
p='project-en/index.html'; s=open(p).read()
starts={'hook':0,'console':7.9,'outputs':47.3,'endcard':60.9}; ends={'hook':8.3,'console':47.7,'outputs':61.3,'endcard':67.9}
for n in starts:
    s=re.sub(r'(id="%s"\s+data-composition-id="%s"\s+data-composition-src="[^"]+"\s+data-start=")[\d.]+("\s+data-duration=")[\d.]+'%(n,n),
             lambda m:m.group(1)+f'{W(starts[n]):g}'+m.group(2)+f'{round(W(ends[n]-1e-3)+1e-3-W(starts[n]),3):g}',s)
s=re.sub(r'(<audio id="(?!music)[^"]+" class="clip" src="[^"]+" data-start=")([\d.]+)"',lambda m:m.group(1)+f'{W(float(m.group(2))):g}"',s)
s=re.sub(r'\{"t":([\d.]+),',lambda m:'{"t":%g,'%W(float(m.group(1))),s)
s=s.replace('data-duration="67.9"',f'data-duration="{W(67.9):g}"')
s=s.replace('data-start="0"\n      data-duration="67.9"',f'data-start="0"\n      data-duration="{W(67.9):g}"')
w=json.load(open('vo-en2/words.json'))
for i in range(1,15):
    s=re.sub(r'(<audio id="vo-%02d" class="clip" src=")assets/vo/n%02d.mp3(" data-start="[\d.]+" data-duration=")[\d.]+'%(i,i),
             lambda m:m.group(1)+f'assets/vo-en/n{i:02d}.mp3'+m.group(2)+f'{w[f"n{i:02d}"]["dur"]:g}',s)
s=s.replace('Doubao seed-tts-2.0, zh_male_liufei_uranus_bigtts','Doubao seed-tts-2.0, en_male_tim_uranus_bigtts')
open(p,'w').write(s)
