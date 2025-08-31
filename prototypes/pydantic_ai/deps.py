from dataclasses import dataclass
from typing import Optional

from protocols.logging_protocol import LoggingProtocol, ProtocolConfig


@dataclass
class HiveDeps:
    session_id: str
    worker: str  # e.g., 'scribe-worker'
    logger: LoggingProtocol
    protocol_version: str = "v1"


def make_logger(session_id: str, worker: str, protocol_version: str = "v1") -> LoggingProtocol:
    cfg = ProtocolConfig(
        {
            "session_id": session_id,
            "agent_name": worker,
            "protocol_version": protocol_version,
        }
    )
    return LoggingProtocol(cfg)
