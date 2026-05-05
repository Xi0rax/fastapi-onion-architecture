class TaskStatsClient:
    async def get_user_task_stats(self, user_id: str) -> dict:
        """
        TODO request-reply via RabbitMQ
        """
        return {
            "assigned_tasks_count": 0,
            "watched_tasks_count": 0,
        }
