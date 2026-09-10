"""Render public GitHub metadata. Default: offline; --refresh: public API."""

import argparse
from collections import Counter
from datetime import date, datetime, timezone
from html import escape
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/github-snapshot.json"
ASSET = ROOT / "assets/github-metrics.svg"
MONTHS = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]


def refresh():
    # No credentials or private endpoints. Accumulate all pages before saving.
    rows = []
    for page in range(1,1001):
        url=f"https://api.github.com/users/dalvadev/repos?type=owner&per_page=100&page={page}"
        req=Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"dalvadev-profile-metrics"})
        with urlopen(req,timeout=30) as response:
            chunk=json.load(response)
        if not isinstance(chunk,list):
            raise ValueError("Expected a repository list; snapshot was not replaced.")
        rows.extend(chunk)
        if len(chunk)<100:
            break
    else:
        raise RuntimeError("Pagination limit reached; snapshot was not replaced.")
    eligible=[r for r in rows if not r["fork"] and not r["private"] and r["owner"]["login"].lower()=="dalvadev" and r["name"].lower()!="dalvadev"]
    eligible.sort(key=lambda r:(r["created_at"],r["name"]))
    output={"login":"dalvadev","as_of":datetime.now(timezone.utc).date().isoformat(),"source":"GitHub REST API","scope":"Repositorios públicos propios accesibles, sin forks ni el repositorio de perfil.","repositories":[{"name":r["name"],"url":r["html_url"],"language":r["language"],"created_at":r["created_at"],"archived":r["archived"]} for r in eligible]}
    return output


def render(data):
    rows=data["repositories"]
    if not rows or len({r["name"].lower() for r in rows})!=len(rows):
        raise ValueError("Expected nonempty unique repositories.")
    cutoff=date.fromisoformat(data["as_of"])
    stamp=f"{cutoff.day:02d} {MONTHS[cutoff.month-1]} {cutoff.year}"
    languages=Counter(r["language"] or "Sin clasificar" for r in rows)
    ordered=sorted(((k,v) for k,v in languages.items() if k!="Sin clasificar"),key=lambda item:(-item[1],item[0]))
    if "Sin clasificar" in languages:
        ordered.append(("Sin clasificar",languages["Sin clasificar"]))
    annual=Counter(int(r["created_at"][:4]) for r in rows)
    years=list(range(min(annual),cutoff.year+1))
    assert sum(languages.values())==sum(annual.values())==len(rows)

    bg,fg,muted,mint,blue="#09151B","#F0F5F2","#B4C8C2","#80E5C5","#96BDFF"
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.fonttype":"none","svg.hashsalt":"dalvadev-metrics","axes.unicode_minus":False})
    fig=plt.figure(figsize=(12.8,7.2),facecolor=bg)
    fig.text(.04,.928,"GITHUB / PUBLIC WORK",color=mint,size=12,weight="bold")
    fig.text(.04,.851,str(len(rows)),color=fg,size=43,weight="bold")
    fig.text(.118,.865,"repositorios públicos propios",color=fg,size=17)
    fig.text(.118,.824,"Proyectos y ejercicios · sin forks ni repositorio de perfil",color=muted,size=10)
    fig.text(.96,.928,stamp,color=muted,size=11,ha="right")
    ax=fig.add_axes([.156,.17,.355,.54],facecolor=bg)
    labels=[x[0] for x in ordered]; values=[x[1] for x in ordered]
    bars=ax.barh(labels,values,color=[mint if k!="Sin clasificar" else "#647D7C" for k in labels],height=.53)
    ax.invert_yaxis(); ax.set_xlim(0,max(values)+1)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=4))
    ax.set_xlabel("Número de repositorios",color=muted,labelpad=13,size=10)
    ax.set_title("Lenguaje principal",color=fg,loc="left",pad=22,size=15,weight="bold")
    for bar,v in zip(bars,values):
        ax.text(v+.12,bar.get_y()+bar.get_height()/2,str(v),color=fg,va="center",size=12,weight="bold")
    bx=fig.add_axes([.61,.17,.345,.54],facecolor=bg)
    vals=[annual.get(y,0) for y in years]
    yearlabels=[str(y)+( "*" if y==cutoff.year else "") for y in years]
    bx.bar(yearlabels,vals,color=[blue if y!=cutoff.year else "#ECCB8E" for y in years],width=.48)
    bx.set_ylim(0,max(vals)*1.25+1)
    bx.yaxis.set_major_locator(MaxNLocator(integer=True,nbins=4))
    bx.set_title("Repositorios creados por año",color=fg,loc="left",pad=22,size=15,weight="bold")
    bx.set_xlabel(f"*{cutoff.year}: hasta el {stamp}",color=muted,labelpad=13,size=10)
    for i,v in enumerate(vals):
        bx.text(i,v+.45,str(v),ha="center",color=fg,size=12,weight="bold")
    for chart in (ax,bx):
        chart.tick_params(colors=muted,length=0,pad=8)
        for spine in chart.spines.values():spine.set_visible(False)
        chart.set_axisbelow(True)
    ax.grid(axis="x",color="#27403F",alpha=.65,linewidth=.7)
    bx.grid(axis="y",color="#27403F",alpha=.65,linewidth=.7)
    fig.text(.04,.043,"Fuente: API pública de GitHub · clasificación automática por repositorio · detalle y método en docs/METRICS.md",color=muted,size=9)
    ASSET.parent.mkdir(exist_ok=True)
    metadata={"Date":data["as_of"],"Creator":"Denis Alva profile / Matplotlib"}
    fig.savefig(ASSET,format="svg",facecolor=bg,metadata=metadata)
    # Reuse the same plotted values in a portrait layout, without reducing data.
    fig.set_size_inches(7.2,11)
    for item in list(fig.texts): item.remove()
    fig.text(.07,.951,"GITHUB / PUBLIC WORK",color=mint,size=13,weight="bold")
    fig.text(.07,.891,str(len(rows)),color=fg,size=42,weight="bold")
    fig.text(.24,.912,"repositorios públicos",color=fg,size=17)
    fig.text(.24,.884,"propios · "+stamp,color=muted,size=12)
    ax.set_position([.26,.485,.63,.315])
    bx.set_position([.15,.10,.73,.285])
    for chart in (ax,bx):
        chart.tick_params(labelsize=12)
        chart.title.set_fontsize(15)
    fig.text(.07,.032,"Fuente: GitHub · sin forks ni repositorio de perfil",color=muted,size=10)
    fig.savefig(ASSET.with_name("github-metrics-mobile.svg"),format="svg",facecolor=bg,metadata=metadata)
    plt.close(fig)
    alt=(f"Corte {stamp}: {len(rows)} repositorios públicos propios, sin forks ni repositorio de perfil. Lenguaje principal: "+", ".join(f"{k} {v}" for k,v in ordered)+". Repositorios creados por año: "+", ".join(f"{y}{' hasta el corte' if y==cutoff.year else ''}: {annual.get(y,0)}" for y in years)+".")
    for asset in (ASSET, ASSET.with_name("github-metrics-mobile.svg")):
        svg=asset.read_text(encoding="utf-8")
        pos=svg.index(">",svg.index("<svg"))+1
        svg=svg[:pos]+f'<title>GitHub en datos · Denis Alva</title><desc>{escape(alt)}</desc>'+svg[pos:]
        asset.write_text(svg,encoding="utf-8")
    readme=ROOT/"README.md"
    body=readme.read_text(encoding="utf-8")
    body=re.sub(r'(<img src="[^"]*/assets/github-metrics\.svg" width="100%" alt=")[^"]*(">)',lambda m:m[1]+escape(alt,quote=True)+m[2],body)
    body=re.sub(r'Fuente: metadatos públicos de GitHub, corte \*\*[^*]+\*\*',f'Fuente: metadatos públicos de GitHub, corte **{stamp}**',body)
    readme.write_text(body,encoding="utf-8")
    docs=ROOT/"docs/METRICS.md"
    content=docs.read_text(encoding="utf-8")
    content=re.sub(r'al \*\*[^*]+\*\*',f'al **{stamp}**',content,count=1)
    docs.write_text(content,encoding="utf-8")
    print(json.dumps({"repositories":len(rows),"languages":dict(ordered),"created_by_year":{y:annual.get(y,0) for y in years},"as_of":data["as_of"]},ensure_ascii=False))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh",action="store_true",help="Refresh metadata from GitHub's public API")
    args=parser.parse_args()
    data=refresh() if args.refresh else json.loads(DATA.read_text(encoding="utf-8"))
    render(data)
    if args.refresh:
        temporary=DATA.with_suffix(".tmp")
        temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        temporary.replace(DATA)
