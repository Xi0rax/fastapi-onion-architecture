__all__ = [
    "TaskStatsClient",
    "UserInfoRpcConsumer",
    "get_channel",
]

from auth_service.src.broker.rabbit import get_channel
from auth_service.src.broker.task_stats_client import TaskStatsClient
from auth_service.src.broker.user_info_rpc import UserInfoRpcConsumer
