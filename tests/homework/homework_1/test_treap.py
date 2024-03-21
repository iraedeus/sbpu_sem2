from random import randint

import pytest

from src.homework.homework_1.treap import *


def create_test_tree(tree_data):
    tree = CartesianTree(root=None)
    for i in tree_data:
        tree[i] = i
    return tree


def check_invariant(tree):
    def recursion(parent: Node, left_child: Node, right_child: Node):
        if left_child is None and right_child is None:
            return True
        if left_child is None:
            is_invariant = right_child.key > parent.key and parent.priority > right_child.priority
            return is_invariant and recursion(right_child, right_child.left, right_child.right)

        if right_child is None:
            is_invariant = left_child.key < parent.key and parent.priority > left_child.priority
            return is_invariant and recursion(left_child, left_child.left, left_child.right)

        if left_child is not None and right_child is not None:
            is_invariant = (
                (parent.priority > left_child.priority and parent.priority > right_child.priority)
                and parent.key > left_child.key
            ) and parent.key < right_child.key
            return (
                is_invariant
                and recursion(left_child, left_child.left, left_child.right)
                and recursion(right_child, right_child.left, right_child.right)
            )

    return recursion(tree.root, tree.root.left, tree.root.right)


@pytest.mark.parametrize("size", [2, 100, 1000, 10000])
def test_setitem(size):
    tree = CartesianTree(root=None)
    for i in range(size):
        tree[randint(1, 1000000)] = randint(1, 10000)

    assert check_invariant(tree)


@pytest.mark.parametrize(
    "tree_data, key, value, expected", [([177, 10, 77], 10, 16, 16), ([177, 323, 5, 88], 88, 16, 16)]
)
def test_setitem_replace(tree_data, key, value, expected):
    tree = create_test_tree(tree_data)
    tree[key] = value
    assert tree[key] == expected


@pytest.mark.parametrize("tree_data, key, expected", [([177, 10, 77], 10, 10), ([177, 323, 5, 88], 88, 88)])
def test_getitem(tree_data, key, expected):
    tree = create_test_tree(tree_data)
    assert tree[key] == expected


@pytest.mark.parametrize("tree_data, key", [([177, 77], 10), ([177, 323, 5], 88)])
def test_getitem_err(tree_data, key):
    tree = create_test_tree(tree_data)
    with pytest.raises(KeyError):
        tree[key]


@pytest.mark.parametrize("tree_data, key", [([177, 10, 77], 10), ([177, 88, 323, 5], 88)])
def test_delitem(tree_data, key):
    tree = create_test_tree(tree_data)
    del tree[key]

    try:
        tree[key]
    except KeyError:
        assert True


@pytest.mark.parametrize("tree_data, key", [([177, 77], 10), ([177, 323, 5], 88)])
def test_delitem_err(tree_data, key):
    tree = create_test_tree(tree_data)
    with pytest.raises(KeyError):
        del tree[key]


@pytest.mark.parametrize("tree_data, expected", [([177, 77], [77, 177]), ([177, 323, 5], [5, 177, 323])])
def test_iter(tree_data, expected):
    tree = create_test_tree(tree_data)
    output = []
    for i in tree:
        output.append(i)
    assert output == expected
