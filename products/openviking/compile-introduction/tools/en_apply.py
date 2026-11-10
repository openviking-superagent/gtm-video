import sys,re,glob
sys.path.insert(0,'tools'); from en_map import M
caps={
"c-cap1":"All your data lives in OpenViking's <em>context tree</em>",
"c-cap2":"Choose <em>Wiki</em>, and describe what you need in one line",
"c-cap3":"Then pick the <em>source folders</em> from the context tree",
"c-cap4":"Compile <em>reads, extracts, and merges</em> in the background",
"c-cap5":"then <em>writes the results back</em> to the context tree",
"c-cap6":"Scattered files become <em>an interlinked Wiki</em>",
"c-cap7":"It also catches <em>conflicts across sources</em>, automatically",
"c-cap8":"Review them on the <em>Kanban board</em>; the fix goes back to the Wiki",
"c-cap9":"Where the conflicts are, and why: <em>all clear on the board</em>",
}
for f in glob.glob('project-en/compositions/*.html')+['project-en/index.html']:
    s=open(f).read()
    for k,v in caps.items():
        s=re.sub(r'(<div class="cap" id="%s">).*?(</div>)'%k, lambda m:m.group(1)+v+m.group(2), s)
    s=s.replace('<span>资料越来越多，</span><span>知识却越来越散</span>','<span>Your docs keep piling up,&nbsp;</span><span>your knowledge keeps scattering</span>')
    s=s.replace('已选<span class="numstack"','<span class="numstack"').replace('</span>个</div>','</span>&nbsp;selected</div>')
    s=s.replace('lang="zh-CN"','lang="en"')
    for k in sorted(M,key=len,reverse=True): s=s.replace(k,M[k])
    open(f,'w').write(s)
