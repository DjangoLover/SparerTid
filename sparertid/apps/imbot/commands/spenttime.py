from sparertid.apps.imbot.bot import IMBot


@IMBot.command_register(
    r'(?P<project>\w+)#(?P<task>[\w\-_.]+)\s+eta\s+(?P<eta>\d{1,2}:\d{1,2})'
)
def create_eta(user, message, **kwargs):
    pass
