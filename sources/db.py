class Database:
    xml = None

    @classmethod
    def create_db(cls):
        from pathlib import Path
        from pydblite import Base

        if not Path('database').exists():
            Path('database').mkdir()

        cls.xml = Base('database/xml.pdl')
        if not cls.xml.exists():
            cls.xml.create('title', 'content')

    @classmethod
    def drop_db(cls):
        import os

        file_path = 'database\\xml.pdl'
        if os.path.exists(file_path):
            os.remove(file_path)

    @classmethod
    def open_db(cls):
        from pydblite import Base

        cls.xml = Base('database/xml.pdl')
        cls.xml.open()
