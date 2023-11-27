from asyncio import get_event_loop_policy, AbstractEventLoop, AbstractEventLoopPolicy
from typing import Generator

import pytest


# SETUP
@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    policy: AbstractEventLoopPolicy = get_event_loop_policy()
    loop: AbstractEventLoop = policy.new_event_loop()
    yield loop
    loop.close()
