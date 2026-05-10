TAG_METADATA = [
    {
        'name': 'tasks',
        'description': 'Operations with tasks.',
    },
    {
        'name': 'boards',
        'description': 'Operations with boards.',
    },
    {
        'name': 'columns',
        'description': 'Operations with board columns.',
    },
    {
        'name': 'sprints',
        'description': 'Operations with sprints.',
    },
    {
        'name': 'groups',
        'description': 'Operations with task_service groups.',
    },
    {
        'name': 'healthz',
        'description': 'Standard health check.',
    },
]

TITLE = 'FastAPI Onion Architecture'
DESCRIPTION = (
    'Implemented on FastAPI.\n\n'
    'Examples taken from the book - https://www.cosmicpython.com/book/chapter_06_uow.html.\n\n'
    'For contact - https://t.me/kalyukov_ns'
)
VERSION = '0.0.1'

ERRORS_MAP = {
    'mongo': 'Mongo connection failed',
    'postgres': 'PostgreSQL connection failed',
    'redis': 'Redis connection failed',
    'rabbit': 'RabbitMQ connection failed',
}
