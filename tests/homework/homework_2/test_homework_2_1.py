from random import randint

import pytest

from src.homework.homework_2.homework_2_1 import *


def create_test_cmd_storage(storage):
    new_stack = Stack(None)
    return PerformedCommandStorage(storage=storage, history=new_stack)


class TestCommandStorage:
    @pytest.mark.parametrize("storage", [({1, 2, 5}), ({111, 5})])
    def test_err_not_indexed(self, storage):
        with pytest.raises(TypeError):
            cmd_storage = create_test_cmd_storage(storage)

    @pytest.mark.parametrize("storage", [([1, 2, 5]), ([111, 5])])
    def test_err_empty_history(self, storage):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.undo()


class TestActionInsertFirst:
    @pytest.mark.parametrize(
        "storage, value, expected",
        [([1, 5, 4, 3], 8, [8, 1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 10, [10, 1, 5, 4, 6, 7, 8, 3])],
    )
    def test_do(self, storage, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertFirst(value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, value_1, value_2, expected",
        [([1, 5, 4, 3], 8, 9, [8, 1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 10, 11, [10, 1, 5, 4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, value_1, value_2, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertFirst(value_1))
        cmd_storage.apply(action=ActionInsertFirst(value_2))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, value", [([1, 2, 5], "ggwp"), ([111, 5], (5, 6))])
    def test_err_not_int(self, storage, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(TypeError):
            cmd_storage.apply(ActionInsertFirst(value))


class TestActionInsertLast:
    @pytest.mark.parametrize(
        "storage, value, expected",
        [([1, 5, 4, 3], 8, [1, 5, 4, 3, 8]), ([1, 5, 4, 6, 7, 8, 3], 10, [1, 5, 4, 6, 7, 8, 3, 10])],
    )
    def test_do(self, storage, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertLast(value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, value_1, value_2, expected",
        [([1, 5, 4, 3], 8, 9, [1, 5, 4, 3, 8]), ([1, 5, 4, 6, 7, 8, 3], 10, 11, [1, 5, 4, 6, 7, 8, 3, 10])],
    )
    def test_undo(self, storage, value_1, value_2, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionInsertLast(value_1))
        cmd_storage.apply(action=ActionInsertLast(value_2))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, value", [([1, 2, 5], "ggwp"), ([111, 5], (5, 6))])
    def test_err_not_int(self, storage, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(TypeError):
            cmd_storage.apply(ActionInsertFirst(value))


class TestActionSwap:
    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 1, [5, 1, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 0, 4, [7, 5, 4, 6, 1, 8, 3])],
    )
    def test_do(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSwap(first_index, second_index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, first_index, second_index, expected",
        [([1, 5, 4, 3], 0, 2, [4, 5, 1, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, 5, [1, 5, 8, 6, 7, 4, 3])],
    )
    def test_undo(self, storage, first_index, second_index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionSwap(first_index, second_index))
        cmd_storage.apply(action=ActionSwap(first_index + 1, second_index + 1))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, first_index, second_index", [([1, 2, 3], 0, 100), ([111, 5], 101, 100)])
    def test_err_no_index(self, storage, first_index, second_index):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionSwap(first_index, second_index))


class TestActionAdd:
    @pytest.mark.parametrize(
        "storage, index, value, expected",
        [([1, 5, 4, 3], 0, 5, [6, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, 4, [1, 5, 4, 6, 7, 12, 3])],
    )
    def test_do(self, storage, index, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionAdd(index, value))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, value, expected",
        [([1, 5, 4, 3], 1, 4, [1, 9, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, 5, [1, 5, 9, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, value, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionAdd(index, value))
        cmd_storage.apply(action=ActionAdd(index, value))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index, value", [([1, 2, 3], 100, 100), ([111, 5], 101, 100)])
    def test_err_no_index(self, storage, index, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionAdd(index, value))


class TestActionFlip:
    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 0, [-1, 5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 5, [1, 5, 4, 6, 7, -8, 3])],
    )
    def test_do(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionFlip(index))
        assert cmd_storage.storage == expected

    @pytest.mark.parametrize(
        "storage, index, expected",
        [([1, 5, 4, 3], 1, [1, -5, 4, 3]), ([1, 5, 4, 6, 7, 8, 3], 2, [1, 5, -4, 6, 7, 8, 3])],
    )
    def test_undo(self, storage, index, expected):
        cmd_storage = create_test_cmd_storage(storage)
        cmd_storage.apply(action=ActionFlip(index))
        cmd_storage.apply(action=ActionFlip(index))
        cmd_storage.undo()

        assert cmd_storage.storage == expected

    @pytest.mark.parametrize("storage, index, value", [([1, 2, 3], 100, 100), ([111, 5], 101, 100)])
    def test_err_no_index(self, storage, index, value):
        cmd_storage = create_test_cmd_storage(storage)
        with pytest.raises(IndexError):
            cmd_storage.apply(ActionAdd(index, value))


class TestActionSquare: ...


class TestActionDeleteSlice: ...


class TestActionPop: ...


class TestActionMove: ...
