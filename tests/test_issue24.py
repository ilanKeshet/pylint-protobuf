import pytest

import pylint_protobuf
from conftest import CheckerTestCase, extract_node


@pytest.fixture
def nested_mod(proto_builder):
    return proto_builder("""
        syntax = "proto3";
        message Outer {
          message Inner {
            string inner_field = 1;
          }
          Inner field = 1;
        }
    """, 'nested')


@pytest.fixture
def nested_plus_enum_mod(proto_builder):
    return proto_builder("""
        syntax = "proto3";
        message Outer {
          enum InnerEnum {
            VALUE = 0;
          }
          message Inner {
            string inner_field = 1;
          }
          Inner field = 1;
        }
    """, 'nested_plus_enum')


class TestNestedMessages(CheckerTestCase):
    CHECKER_CLASS = pylint_protobuf.ProtobufDescriptorChecker

    def test_nested_message_definition_does_not_warn(self, nested_mod):
        self.assert_no_messages(extract_node("""
            from {} import Outer
            inner = Outer.Inner(inner_field='foo')  #@
        """.format(nested_mod)))

    @pytest.mark.xfail(reason='unfixed issue #24')
    def test_nested_message_with_unrelated_enum_does_not_warn(self, nested_plus_enum_mod):
        self.assert_no_messages(extract_node("""
            from {} import Outer
            inner = Outer.Inner(inner_field='foo')  #@
        """.format(nested_plus_enum_mod)))