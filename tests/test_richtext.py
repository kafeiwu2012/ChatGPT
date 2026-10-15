"""Run: python -m unittest discover -s tests -v (no third-party packages)."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]/'PortableBlog'
sys.path.insert(0,str(ROOT))
from richtext import sanitize, typography

class RichTextTests(unittest.TestCase):
    def test_formatting_survives(self):
        html,refs=sanitize('<h2>标题</h2><p class="ql-align-center"><strong>重点</strong><span style="color:#a58045;background-color:rgb(250,240,220)">文字</span></p><blockquote>引用</blockquote><ul><li>项目</li></ul>')
        self.assertIn('<h2>标题</h2>',html)
        self.assertIn('ql-align-center',html)
        self.assertIn('color:#a58045',html)
        self.assertIn('<ul><li>项目</li></ul>',html)
        self.assertEqual(refs,[])

    def test_executable_content_is_removed(self):
        html,_=sanitize('<script>alert(1)</script><svg onload="x"><script>x</script></svg><p onclick="x" style="position:fixed;background:url(https://evil);color:red">safe</p>')
        self.assertEqual(html,'<p style="color:red">safe</p>')

    def test_unsafe_links_removed(self):
        html,_=sanitize('<a href="javascript:alert(1)" onmouseover="x">bad</a><a href="https://example.com">good</a>')
        self.assertNotIn('javascript',html)
        self.assertNotIn('onmouseover',html)
        self.assertIn('rel="noopener noreferrer"',html)

    def test_only_local_media_can_embed(self):
        key='a'*32
        html,refs=sanitize('<img src="https://evil/image.png"><img src="data:image/png;base64,AAAA"><iframe src="https://evil"></iframe><video src="/media/'+key+'" autoplay onerror="x"></video>')
        self.assertNotIn('evil',html)
        self.assertNotIn('data:',html)
        self.assertNotIn('autoplay',html)
        self.assertIn('controls=""',html)
        self.assertEqual(refs,[key])

    def test_references_are_deduplicated(self):
        key='b'*32
        html,refs=sanitize('<img src="/media/'+key+'"><a href="/media/'+key+'">file</a><img src="/assets/cover.svg">')
        self.assertEqual(refs,[key])
        self.assertIn('/assets/cover.svg',html)

    def test_entities_remain_text(self):
        html,_=sanitize('<p>&lt;script&gt; &amp; 你好</p>')
        self.assertEqual(html,'<p>&lt;script&gt; &amp; 你好</p>')

    def test_typography_limits(self):
        self.assertEqual(json.loads(typography({'font':'serif','size':20,'line':2.2,'spacing':'airy'}))['size'],20)
        for data in ({'size':100},{'font':'url(evil)'},{'line':999},{'spacing':'invalid'},[]):
            with self.assertRaises(ValueError):typography(data)

    def test_v2_database_upgrade_keeps_plain_content(self):
        # Legacy literal markup must remain plain text until edited and explicitly saved as HTML.
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'blog.py').write_bytes((ROOT/'blog.py').read_bytes())
            (root/'richtext.py').write_bytes((ROOT/'richtext.py').read_bytes())
            (root/'data').mkdir()
            with sqlite3.connect(root/'data/blog.sqlite3') as c:
                c.executescript('CREATE TABLE settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);CREATE TABLE posts(id TEXT PRIMARY KEY,title TEXT NOT NULL,body TEXT NOT NULL,category TEXT NOT NULL,status TEXT NOT NULL,created TEXT NOT NULL,updated TEXT NOT NULL,attachments TEXT NOT NULL);CREATE TABLE pages(slug TEXT PRIMARY KEY,title TEXT NOT NULL,body TEXT NOT NULL,attachments TEXT NOT NULL,status TEXT NOT NULL);')
                c.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',('old','旧文章','<b>这是原文</b>\n第二行','生活记录','published','2020','2020','[]'))
                c.execute('INSERT INTO pages VALUES (?,?,?,?,?)',('about','旧关于','原有页面正文','[]','published'))
                c.execute('INSERT INTO settings VALUES (?,?)',('password',json.dumps({'salt':'preserve','hash':'preserve'})))
            spec=importlib.util.spec_from_file_location('migration_fixture',root/'blog.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            module.init();module.init()
            with module.connect() as c:
                row=c.execute("SELECT body,format,typography FROM posts WHERE id='old'").fetchone()
                self.assertEqual(tuple(row),('<b>这是原文</b>\n第二行','plain','{}'))
                self.assertEqual(c.execute("SELECT body FROM pages WHERE slug='about'").fetchone()[0],'原有页面正文')
            self.assertEqual(module.setting('password'),{'salt':'preserve','hash':'preserve'})

if __name__=='__main__':unittest.main()
