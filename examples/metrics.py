from datetime import datetime, timedelta, timezone

from bytewax.connectors.stdio import StdOutput
from bytewax.dataflow import Dataflow
from bytewax.inputs import PartitionedInput, StatefulSource
from bytewax.testing import TestingInput
from bytewax.tracing import setup_tracing

setup_tracing(log_level="TRACE")


class _SlowSource(StatefulSource):
    def __init__(self, sleep: timedelta, resume_state):
        self._last_emit = datetime.now(timezone.utc) - sleep
        self._sleep = sleep
        self._idx = resume_state or -1

    def next(self):
        now = datetime.now(timezone.utc)
        if now - self._last_emit > self._sleep:
            self._idx += 1
            self._last_emit = now
            return self._idx
        else:
            return None

    def snapshot(self):
        return self._idx


class SlowInput(PartitionedInput):
    def __init__(self, sleep: timedelta):
        self._sleep = sleep

    def list_parts(self):
        return {"iter"}

    def build_part(self, for_key, resume_state):
        assert for_key == "iter"
        return _SlowSource(self._sleep, resume_state)


flow = Dataflow()
flow.input("inp", SlowInput(timedelta(seconds=2)))
flow.output("out", StdOutput())
