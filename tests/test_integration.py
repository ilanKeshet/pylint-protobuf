import os.path

import pytest

import pylint_protobuf

try:
    import google.protobuf
except ImportError:
    pytest.fail('behaviour of E1101 differs if protobuf is not installed')


@pytest.fixture
def e1101_mod(module_builder):
    return module_builder("""
        from person_pb2 import Person

        person = Person()
        print(person.name)  # should not raise E1101
        print(person.should_warn)  # should raise E5901

        class Foo: pass
        Person = Foo  # FIXME: should be renamed by class def
        person = Person()
        print(person.renamed_should_warn)  # should raise E1101
    """, 'e1101')


EXPECTED_MSGS = [
    pylint_protobuf.MESSAGES['E5901'][0] % ('should_warn', 'person_pb2.Person'),
    "Instance of 'Foo' has no 'renamed_should_warn' member",
]


def test_no_E1101_on_protobuf_classes(e1101_mod, linter_factory):
    linter = linter_factory(
        register=pylint_protobuf.register,
        disable=['all'], enable=['protobuf-undefined-attribute', 'no-member'],
    )
    linter.check([e1101_mod])
    actual_msgs = [message.msg for message in linter.reporter.messages]
    assert sorted(EXPECTED_MSGS) == sorted(actual_msgs)
