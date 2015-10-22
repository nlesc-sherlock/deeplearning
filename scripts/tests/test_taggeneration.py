from taggeneration.taggenerator import (generate_tags)
import unittest
from nose.tools import assert_equal, assert_equals, assert_true, assert_in

def test_returns_iterable():
    out = generate_tags(None)
    assert_equal(len(out), 0)

def test_cat_image_returns_cat_tag():
    path_to_cat_image = "data/cat.jpg"
    out = generate_tags(path_to_cat_image)
    assert_in('cat', out)
