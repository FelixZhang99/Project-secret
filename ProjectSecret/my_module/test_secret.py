import pytest

import Secret

def test_getTree():
    node1 = node(None, None, 10, 'e')
    node2 = ndoe(None, None, 20, 'a')
    my_list = [node2, node1]
    new_node = getTree(my_list)
    assert new_node.value == 30
    assert new_node.letter == None
    assert new_node.left.letter == 'e'
    assert new_node.right.letter == 'a'

