"""Only read the approved STATIC SVG artwork. No previous animation is read."""
from pathlib import Path
from copy import deepcopy
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / '2026-10-14-blue-style' / '01_当前定稿'
OUT = HERE / 'assets'
OUT.mkdir(exist_ok=True)
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])

def write_svg(name, root, children):
    fresh = ET.Element(NS+'svg', {k: v for k, v in root.attrib.items() if k in ['width','height','viewBox']})
    defs=root.find(NS+'defs')
    if defs is not None:
        fresh.append(deepcopy(defs))
    for child in children:
        fresh.append(deepcopy(child))
    ET.ElementTree(fresh).write(OUT / (name+'.svg'), encoding='utf-8', xml_declaration=True)

title = ET.parse(next(BASE.glob('01_*/assets/title-final-transparent.svg'))).getroot()
logo = title.find(NS+'g')
for i,glyph in enumerate(list(logo[0])):
    write_svg('glyph-'+str(i),title,[glyph])
write_svg('english',title,[logo[1]])
write_svg('title',title,[logo])

eye = ET.parse(next(BASE.glob('02_*/assets/eyecatch-pause.svg'))).getroot()
glyphs = eye.findall(NS+'g')[-4:]
for i,glyph in enumerate(glyphs):
    write_svg('eye-'+str(i),eye,[glyph])
print('Prepared 14 static SVG assets, without reading any existing animation.')
