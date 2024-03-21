import copy
from collections.abc import Mapping, MutableMapping
from random import random
from typing import Any, Iterator, Optional


class Node:
    def __init__(self, key: int, value: Any, priority: float, left: Optional["Node"], right: Optional["Node"]) -> None:
        self.key: int = key
        self.value: Any = value
        self.priority: float = priority
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        return self.key == other.key and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        return not (self == other)


class CartesianTree(MutableMapping, Mapping):
    def __init__(self, root: Optional[Node], length: int = 0) -> None:
        self.root: Optional[Node] = root
        self.length: int = length

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: int) -> Any:
        first_tree, subtree = split(self, key)
        output_tree, second_tree = split(subtree, key + 1)

        if output_tree.root is None:
            raise KeyError
        else:
            value = output_tree.root.value
            return value

    def __setitem__(self, key: int, value: Any) -> None:
        first_tree, subtree = split(self, key)
        node_tree, second_tree = split(subtree, key + 1)

        new_node = Node(key, value, random(), None, None)
        node_tree.root = new_node

        output_tree = merge(merge(first_tree, node_tree), second_tree)

        self.root = output_tree.root
        self.length += 1

    def __delitem__(self, key: int) -> None:
        first_tree, subtree = split(self, key)
        node_tree, second_tree = split(subtree, key + 1)

        if node_tree.root is None:
            raise KeyError
        else:
            del node_tree
            output_tree = merge(first_tree, second_tree)

        self.root = output_tree.root
        self.length -= 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CartesianTree):
            return NotImplemented
        if self.length != other.length:
            return False
        if self.root != other.root:
            return False

        def recursion(first_node: Optional[Node], second_node: Optional[Node]) -> bool:
            if first_node is None and second_node is None:
                return True
            if first_node is None or second_node is None:
                return False

            return (
                first_node == second_node
                and recursion(first_node.left, second_node.left)
                and recursion(first_node.right, second_node.right)
            )

        return recursion(self.root, other.root)

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, CartesianTree):
            return NotImplemented
        return not (self == other)

    def __iter__(self) -> Iterator:
        if self.root is None:
            return iter([])

        output: list[int] = []

        def recursion(current_node: Node, nodes: list) -> None:
            if current_node.left is not None:
                recursion(current_node.left, nodes)
            nodes.append(current_node.key)
            if current_node.right is not None:
                recursion(current_node.right, nodes)

        recursion(self.root, output)

        return iter(output)


def merge_nodes(lower_node: Optional[Node], higher_node: Optional[Node]) -> Optional[Node]:
    if lower_node is None:
        return higher_node
    if higher_node is None:
        return lower_node

    if lower_node.priority > higher_node.priority:
        node = lower_node
        node.right = merge_nodes(node.right, higher_node)

        return node
    else:
        node = higher_node
        node.left = merge_nodes(lower_node, higher_node.left)

        return node


def merge(lower_tree: CartesianTree, higher_tree: CartesianTree) -> CartesianTree:
    node = merge_nodes(lower_tree.root, higher_tree.root)
    return CartesianTree(root=node)


def split_nodes(node: Optional[Node], key: int) -> tuple[Optional[Node], Optional[Node]]:
    if node is None:
        return None, None

    lower_node: Optional[Node]
    higher_node: Optional[Node]

    node_copy = copy.copy(node)

    if node_copy.key < key:
        lower_node = node_copy
        left_subnode, higher_node = split_nodes(lower_node.right, key)

        lower_node.right = left_subnode

    else:
        higher_node = node_copy
        lower_node, right_subnode = split_nodes(higher_node.left, key)

        higher_node.left = right_subnode

    return lower_node, higher_node


def split(tree: CartesianTree, key: int) -> tuple[CartesianTree, CartesianTree]:
    lower_node, higher_node = split_nodes(tree.root, key)
    return CartesianTree(root=lower_node), CartesianTree(root=higher_node)
