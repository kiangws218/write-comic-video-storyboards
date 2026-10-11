from pathlib import Path

out=Path(__file__).resolve().parent
p=out/'第18话_前15格_完整分镜_Gen2.8.1.md'
s=p.read_text(encoding='utf-8')
s=s.replace('岩壁采用低饱和蓝灰色','岩壁采用低饱和深褐色')
s=s.replace('洞窟岩石为蓝灰色、石缝为深灰蓝','洞窟岩石为深褐色、石缝为深褐黑')
s=s.replace('蓝灰岩壁','深褐岩壁').replace('蓝灰岩面','深褐岩面').replace('蓝灰岩块','深褐岩块')
s=s.replace('蓝灰岩','深褐岩')
p.write_text(s,encoding='utf-8')
print('Environment base palette follows the inspected workspace ep018 005_003 colored rock; cold lighting remains local shading.')
