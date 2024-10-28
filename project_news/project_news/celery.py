import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_news.settings')
 
app = Celery('project_news')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'weekly_newsletter_task_every_Monday_at_08_00': {
        'task': 'news_portal.tasks.weekly_newsletter_task',
        'schedule': crontab(hour=8, minute=00, day_of_week='mon'),
    },
}
