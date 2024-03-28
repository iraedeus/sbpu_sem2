from typing import Mapping

import pytest

from src.homework.homework_1.registry import *

dummy_mapping = Registry[Mapping](default=dict)
dummy_mapping_for_errors = Registry[Mapping](default=None)


@dummy_mapping_for_errors.register(name="sussy_dummy")
@dummy_mapping.register(name="dummy")
class Dummy(Mapping):
    pass


class TestDispatch:
    def test_dispatch(self):
        test_class = dummy_mapping.dispatch("dummy")
        assert issubclass(test_class, Mapping)

    def test_dispatch_default(self):
        test_object = dummy_mapping.dispatch("unknown")()
        assert isinstance(test_object, dict)


class TestRegistryErr:
    def test_dispatch_err(self):
        with pytest.raises(ValueError):
            test1 = dummy_mapping_for_errors.dispatch("unknown class")()

    def test_already_exist_err(self):
        with pytest.raises(AlreadyExistError):

            @dummy_mapping.register(name="dummy")
            class Another_Dummy(Mapping):
                pass
