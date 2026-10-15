from pathlib import Path
from PIL import Image
import json

out = Path(__file__).resolve().parent
source = out / 'source-originals' / '第18話_04_001.jpg'
image = Image.open(source)
regions = [('第18話_04_001_上格.jpg', (0, 90, 1080, 685)),
           ('第18話_04_001_下格.jpg', (0, 1220, 1080, 2134))]
records = []
for name, box in regions:
    part = image.crop(box)
    part.save(out / 'source-originals' / name, quality=98)
    part.thumbnail((1280, 720))
    part.save(out / 'analysis-proxies' / name, quality=95)
    records.append({'image': name, 'source_file': source.name, 'box': box,
                    'purpose': '拆出原文件实际上下两格，未改变叙事图像内容',
                    'size': list(part.size)})
(out / 'source-regions.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
print('Separated two comic panels from the composite source file.')
