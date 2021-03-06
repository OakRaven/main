# Test the module type
import unittest
from test.test_support import run_unittest

from test import test_support
import sys
ModuleType = type(sys)

class ModuleTests(unittest.TestCase):
    def test_uninitialized(self):
        # An uninitialized module has no __dict__ or __name__,
        # and __doc__ is None
        foo = ModuleType.__new__(ModuleType)
        if not test_support.due_to_ironpython_bug("http://tkbgitvstfat01:8080/WorkItemTracking/WorkItem.aspx?artifactMoniker=410803"):
            self.assertTrue(foo.__dict__ is None)
            self.assertRaises(SystemError, dir, foo)
            try:
                s = foo.__name__
                self.fail("__name__ = %s" % repr(s))
            except AttributeError:
                pass
        self.assertEqual(foo.__doc__, ModuleType.__doc__)

    def test_no_docstring(self):
        # Regularly initialized module, no docstring
        foo = ModuleType("foo")
        if not test_support.due_to_ironpython_bug("http://tkbgitvstfat01:8080/WorkItemTracking/WorkItem.aspx?artifactMoniker=316514"):
            self.assertEqual(foo.__name__, "foo")
            self.assertEqual(foo.__doc__, None)
            self.assertEqual(foo.__dict__, {"__name__": "foo", "__doc__": None})

    def test_ascii_docstring(self):
        # ASCII docstring
        foo = ModuleType("foo", "foodoc")
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo.__doc__, "foodoc")
        self.assertEqual(foo.__dict__,
                         {"__name__": "foo", "__doc__": "foodoc"})

    def test_unicode_docstring(self):
        # Unicode docstring
        foo = ModuleType("foo", u"foodoc\u1234")
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo.__doc__, u"foodoc\u1234")
        self.assertEqual(foo.__dict__,
                         {"__name__": "foo", "__doc__": u"foodoc\u1234"})

    def test_reinit(self):
        # Reinitialization should not replace the __dict__
        foo = ModuleType("foo", u"foodoc\u1234")
        foo.bar = 42
        d = foo.__dict__
        foo.__init__("foo", "foodoc")
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo.__doc__, "foodoc")
        self.assertEqual(foo.bar, 42)
        self.assertEqual(foo.__dict__,
              {"__name__": "foo", "__doc__": "foodoc", "bar": 42})
        if test_support.due_to_ironpython_bug("http://www.codeplex.com/IronPython/WorkItem/View.aspx?WorkItemId=21116"):
            return
        self.assertTrue(foo.__dict__ is d)

    def test_dont_clear_dict(self):
        # See issue 7140.
        def f():
            foo = ModuleType("foo")
            foo.bar = 4
            return foo
        self.assertEqual(f().__dict__["bar"], 4)

def test_main():
    run_unittest(ModuleTests)

if __name__ == '__main__':
    test_main()
