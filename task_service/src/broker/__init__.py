__all__ = [
    'TaskStatsRpcConsumer',
    'AuthUserClient',
    'get_channel',
]

from task_service.src.broker.auth_user_client import AuthUserClient
from task_service.src.broker.rabbit import get_channel
from task_service.src.broker.task_stats_rpc import TaskStatsRpcConsumer
