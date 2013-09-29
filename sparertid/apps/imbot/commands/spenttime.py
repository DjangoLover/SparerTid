import threading
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _

from sparertid.apps.imbot.bot import IMBot
from sparertid.apps.imbot.forms import SpentTimeForm
from sparertid.apps.imbot.utils import collect_form_errors
from sparertid.apps.project.models import SpentTime


def ping(spent_time_pk):
    spent_time = None
    try:
        spent_time = SpentTime.objects.get(pk=spent_time_pk)
    except SpentTime.DoesNotExist:
        return

    if spent_time.finished_at:
        return

    IMBot().send_message(
        spent_time.user.jid,
        _(u'%s#%s is out date') % (spent_time.project, spent_time.task)
    )

def set_ping_timer(spenttime):
    now = timezone.localtime(timezone.now())
    delay = spenttime.eta - now
    timer = threading.Timer(
        delay.total_seconds(),
        ping,
        args=(spenttime.pk, )
    )
    timer.start()

@IMBot.command_register(
    r'(?P<project>\w+)#(?P<task>[\w\-_.]+)\s+eta\s+(?P<eta>\d{1,2}:\d{1,2})'
)
def create_eta(user, message, **kwargs):
    now = timezone.localtime(timezone.now())
    kwargs['user'] = user.pk
    kwargs['started_at'] = now.strftime(settings.DATETIME_INPUT_FORMATS[0])
    kwargs['eta'] = now.strftime('%Y-%m-%d ') + kwargs['eta']
    form = SpentTimeForm(kwargs)

    if form.is_valid():
        spenttime = form.save()
        set_ping_timer(spenttime)

        return '%s#%s expected at %s' % (
            spenttime.project,
            spenttime.task,
            spenttime.eta.strftime('%Y/%m/%d %H:%M')
        )

    return collect_form_errors(form)

@IMBot.command_register(r'eta\s+done')
def finish_eta(user, message, **kwargs):
    try:
        spenttime = SpentTime.objects.get(user=user, finished_at__isnull=True)
    except SpentTime.DoesNotExist:
        return 'current eta not exist'

    spenttime.finish()

    return '%s#%s finished at %s' % (
        spenttime.project,
        spenttime.task,
        timezone.localtime(spenttime.finished_at).strftime('%Y/%m/%d %H:%M')
    )

@IMBot.command_register(r'eta \+(?P<time>\d+[mh])')
def prolong_eta(user, message, **kwargs):
    types = {'m': 'minutes', 'h': 'hours'}
    try:
        spenttime = SpentTime.objects.get(user=user, finished_at__isnull=True)
    except SpentTime.DoesNotExist:
        return 'current eta not exist'

    time = int(kwargs['time'][:-1])
    tp = kwargs['time'][-1]
    params = {types[tp]: time}

    spenttime.eta += timedelta(**params)
    spenttime.save()

    set_ping_timer(spenttime)

    return '%s#%s expected at %s' % (
        spenttime.project,
        spenttime.task,
        timezone.localtime(spenttime.eta).strftime('%Y/%m/%d %H:%M')
    )
