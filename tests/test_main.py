import unittest
from main import audit

def entry(path='/demo/file',mode='0644',kind='file'): return dict(path=path,mode=mode,kind=kind)
class Tests(unittest.TestCase):
    def test_regular(self): self.assertEqual(audit([entry()]),[])
    def test_world_writable(self): self.assertIn('world_writable',audit([entry(mode='0666')])[0]['reasons'])
    def test_sticky(self): self.assertEqual(audit([entry('/tmp','1777','directory')])[0]['reasons'],['world_writable_sticky_directory_review'])
    def test_setuid(self): self.assertIn('setuid',audit([entry(mode='4755')])[0]['reasons'])
    def test_private_file(self): self.assertIn('private_file_accessible_to_group_or_others',audit([entry('/demo/.env')])[0]['reasons'])
    def test_private_mode(self): self.assertEqual(audit([entry('/demo/id_rsa','0600')]),[])
    def test_invalid_mode(self):
        with self.assertRaises(ValueError): audit([entry(mode='0888')])
