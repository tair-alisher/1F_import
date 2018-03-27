from pathlib import Path
from pydblite import Base

if not Path('database').exists():
    Path('database').mkdir()

xml = Base('database/xml.pdl')
if xml.exists():
    xml.open()
else:
    xml.create('title', 'content')