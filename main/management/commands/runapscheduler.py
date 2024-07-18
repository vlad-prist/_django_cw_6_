from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
# BlockingScheduler Блокирует терминал, в отличии от BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from apscheduler.schedulers.jobstores import DjangoJobStore
from apscheduler.schedulers.models import DjangoJobExecution
from apscheduler.schedulers import util
from main.services import send_all_mails
# завершить ctrl+C


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_all_mails,
            trigger=CronTrigger(second="*/30"),  # Every 30 seconds
            id="sendmail",
            max_instances=10,
            replace_existing=True,
        )

        try:
            print("Starting scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopped scheduler")
            scheduler.shutdown()
            print("Success!")