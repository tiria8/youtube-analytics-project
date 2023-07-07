import pytest
from src.channel import Channel


@pytest.fixture
def channel():
    return Channel('UC-OVMPlMA3-YCIeg4z5z23A')


def test_print_info(channel):
    assert isinstance(channel.print_info(), type(None))

