from django.core.management.base import NoArgsCommand

from sparertid.apps.imbot.bot import IMBot


class Command(NoArgsCommand):
    help = 'start im bot'

    def handle_noargs(self, **options):
        bot = IMBot()
        bot.start()
