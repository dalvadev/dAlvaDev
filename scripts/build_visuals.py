"""Create the profile's original, self-contained vector artwork (Python 3)."""

from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
INK, WHITE, MINT, BLUE, GOLD = "#09151B", "#F0F5F2", "#80E5C5", "#96BDFF", "#ECCB8E"


def text(x, y, value, size=18, fill=WHITE, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def document(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#09151B"/><stop offset="1" stop-color="#112B2C"/></linearGradient>
 <radialGradient id="aura"><stop stop-color="#80E5C5" stop-opacity=".11"/><stop offset="1" stop-color="#80E5C5" stop-opacity="0"/></radialGradient>
 <linearGradient id="signal"><stop stop-color="#80E5C5" stop-opacity=".08"/><stop offset=".65" stop-color="#80E5C5"/><stop offset="1" stop-color="#ECCB8E"/></linearGradient>
 <clipPath id="bounds"><rect width="{width}" height="{height}" rx="24"/></clipPath>
</defs>
<style>
 text {{font-family: 'Segoe UI', Arial, sans-serif}}
 .mono {{font-family: Consolas, 'Liberation Mono', monospace;letter-spacing:2px}}
 .float {{animation: float 10s ease-in-out infinite}}
 .pulse {{animation: pulse 5s ease-in-out infinite}}
 .pulse2 {{animation: pulse 5s ease-in-out -2.5s infinite}}
 .signal {{stroke-dasharray:14 140;animation: signal 18s linear infinite}}
 .scan {{stroke-dasharray:100 1100;animation: signal 24s linear infinite}}
 @keyframes float {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
 @keyframes pulse {{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
 @keyframes signal {{to{{stroke-dashoffset:-1200}}}}
 @media (prefers-reduced-motion:reduce) {{.float,.pulse,.pulse2,.signal,.scan{{animation:none!important}}}}
</style>
<g clip-path="url(#bounds)"><rect width="{width}" height="{height}" fill="url(#bg)"/>{body}</g>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="24" fill="none" stroke="#284345"/>
</svg>'''


def terrain(cx, cy, scale=1):
    def project(u, v):
        z = .95 * math.exp(-((u+.14)**2*4+(v-.08)**2*4))
        z += .3 * math.exp(-((u-.6)**2*12+(v+.5)**2*10))
        return cx+scale*(185*u-113*v), cy+scale*(53*u+57*v-144*z)
    out = ['<g class="float" fill="none">']
    for axis in (0, 1):
        for line in range(21):
            v = -1+line/10
            points = [project(-1+i/30, v) if axis == 0 else project(v, -1+i/30) for i in range(61)]
            path = "M"+" L".join(f"{x:.2f},{y:.2f}" for x,y in points)
            opacity = .20 + .18*(1-abs(v))
            out.append(f'<path d="{path}" stroke="{MINT}" stroke-width="{scale:.2f}" opacity="{opacity:.2f}"/>')
            if axis == 0 and line == 11:
                out.append(f'<path d="{path}" stroke="{MINT}" stroke-width="{2*scale}" class="scan"/>')
    for n,(u,v) in enumerate([(-.7,-.4),(-.2,.2),(.65,.2),(.35,-.7)]):
        x,y=project(u,v)
        c=MINT if n%2==0 else GOLD
        out.append(f'<path d="M{x},{y}v{-30*scale}" stroke="{c}" opacity=".5"/>')
        out.append(f'<circle cx="{x}" cy="{y-30*scale}" r="{4*scale}" fill="{c}"/>')
        out.append(f'<circle cx="{x}" cy="{y-30*scale}" r="{11*scale}" stroke="{c}" opacity=".3" class="pulse{2 if n%2 else ""}"/>')
    out.append('</g>')
    return ''.join(out)


def hero(mobile=False):
    w,h=(720,760) if mobile else (1280,450)
    b=[]
    b.append(f'<ellipse cx="{w*.78}" cy="{h*.44}" rx="350" ry="260" fill="url(#aura)"/>')
    for i in range(28):
        x=(i*131+31)%w; y=(i*79+23)%(h-50)
        b.append(f'<circle cx="{x}" cy="{y}" r="1" fill="#B1D6CA" opacity=".20"/>')
    x=44 if mobile else 58
    b.append(f'<path d="M{x},58v-22h14q16,11,0,22z M{x+38},58l10,-22 10,22 M{x+42},51h13" fill="none" stroke="{MINT}" stroke-width="2"/>')
    b.append(text(x+82,52,"ENGINEERING × DATA × PURPOSE",13 if mobile else 14,MINT,extra='class="mono"'))
    b.append(text(x,160 if mobile else 167,"DENIS ALVA",82 if mobile else 98,WHITE,700,extra='letter-spacing="-4"'))
    if mobile:
        b.extend([text(x,218,"Ingeniería que conecta",30),text(x,260,"datos, software y territorio.",30),text(x,306,"INGENIERO INDUSTRIAL · UNHEVAL",16,"#AAC4BE",extra='class="mono"')])
        b.append(terrain(372,565,.96))
        b.append(text(44,647,"DEL CONTEXTO A LA EVIDENCIA",14,MINT,extra='class="mono"'))
        b.append('<path d="M44 684H676" stroke="#30494A"/>')
        b.append(text(44,724,"HUÁNUCO, PERÚ",15,"#C9DAD3",extra='class="mono"'))
        b.append(text(676,724,"@dalvadev",15,MINT,extra='text-anchor="end" class="mono"'))
    else:
        b.extend([text(x,233,"Ingeniería que conecta",33),text(x,279,"datos, software y territorio.",33),text(x,333,"INGENIERO INDUSTRIAL · UNHEVAL",16,"#AAC4BE",extra='class="mono"')])
        b.append(terrain(973,271,.86))
        b.append(text(1198,58,"FIELD / SYSTEMS / EVIDENCE",12,"#AAC4BE",extra='text-anchor="end" class="mono"'))
        b.append(text(1198,360,"DEL CONTEXTO A LA EVIDENCIA",12,MINT,extra='text-anchor="end" class="mono"'))
        b.append('<path d="M58 386H1222" stroke="#30494A"/>')
        b.append(text(58,423,"HUÁNUCO, PERÚ",14,"#C9DAD3",extra='class="mono"'))
        b.append(text(475,423,"SOFTWARE / DATA / RESEARCH",14,"#C9DAD3",extra='class="mono"'))
        b.append(text(1222,423,"@dalvadev",14,MINT,extra='text-anchor="end" class="mono"'))
    return document(w,h,"Denis Alva · Ingeniería, datos y propósito","Portada con una superficie topográfica conceptual, señales de datos y movimiento sutil. Huánuco, Perú.",''.join(b))


def work_map():
    b=[text(44,45,"UN PERFIL, CUATRO CONEXIONES",13,MINT,extra='class="mono"')]
    paths=["M340,110 C410,110 406,164 454,164","M700,110 C628,110 640,164 586,164","M340,240 C415,240 397,184 454,184","M700,240 C628,240 637,184 586,184"]
    for p in paths:
        b.append(f'<path d="{p}" fill="none" stroke="#345452" stroke-width="1.5"/>')
        b.append(f'<path d="{p}" fill="none" stroke="{MINT}" stroke-width="2" class="signal"/>')
    b.append('<circle cx="520" cy="176" r="76" fill="#102629" stroke="#3B7065"/>')
    b.append('<circle cx="520" cy="176" r="65" fill="none" stroke="#21473F" stroke-dasharray="2 8"/>')
    b.append(text(520,171,"SOLUCIONES",15,MINT,600,extra='text-anchor="middle" letter-spacing="1"'))
    b.append(text(520,196,"útiles",28,WHITE,600,extra='text-anchor="middle"'))
    cards=[(44,76,"01","Ingeniería + gestión","Procesos · proyectos · articulación",MINT),(700,76,"02","Software + automatización","Aplicaciones · flujos · experiencia",BLUE),(44,208,"03","Datos + evidencia","Modelos · indicadores · decisiones",BLUE),(700,208,"04","Territorio + comunidad","RSU · educación · agroecosistemas",GOLD)]
    for x,y,num,title,desc,c in cards:
        b.append(f'<rect x="{x}" y="{y}" width="296" height="97" rx="12" fill="#112327" stroke="#294444"/>')
        b.append(text(x+18,y+25,num,12,c,extra='class="mono"'))
        b.append(text(x+18,y+51,title,17,WHITE,600))
        b.append(text(x+18,y+77,desc,13,"#B2C7C1"))
    return document(1040,336,"Mi enfoque de trabajo","Ingeniería, software, datos y territorio se conectan en el diseño de soluciones útiles. Mapa conceptual.",''.join(b))


def work_map_mobile():
    b=[text(40,54,"UN PERFIL, CUATRO CONEXIONES",18,MINT,extra='class="mono"')]
    cards=[("01","Ingeniería + gestión","Procesos · proyectos · articulación",MINT),("02","Software + automatización","Aplicaciones · flujos · experiencia",BLUE),("03","Datos + evidencia","Modelos · indicadores · decisiones",BLUE),("04","Territorio + comunidad","RSU · educación · agroecosistemas",GOLD)]
    b.append('<path d="M64 146V603" stroke="#315752" fill="none" stroke-width="2"/>')
    b.append(f'<path d="M64 146V603" stroke="{MINT}" fill="none" stroke-width="2" class="signal"/>')
    for i,(num,title,desc,c) in enumerate(cards):
        y=96+i*138
        b.append(f'<circle cx="64" cy="{y+53}" r="7" fill="{c}"/>')
        b.append(f'<rect x="98" y="{y}" width="582" height="110" rx="12" fill="#112327" stroke="#294444"/>')
        b.append(text(120,y+28,num,16,c,extra='class="mono"'))
        b.append(text(120,y+61,title,26,WHITE,600))
        b.append(text(120,y+90,desc,20,"#B2C7C1"))
    b.append(text(360,680,"Diseñar soluciones útiles.",29,MINT,600,extra='text-anchor="middle"'))
    return document(720,720,"Mi enfoque de trabajo","Cuatro ámbitos integrados: ingeniería, software, datos y territorio.",''.join(b))


if __name__ == "__main__":
    for name,body in [("hero.svg",hero()),("hero-mobile.svg",hero(True)),("work-map.svg",work_map()),("work-map-mobile.svg",work_map_mobile())]:
        (ASSETS/name).write_text(body,encoding="utf-8")
        print(f"Generated assets/{name}")
