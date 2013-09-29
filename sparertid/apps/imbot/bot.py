import json
import re
import os
import sys
import threading
import redis
import xmpp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext as _


IMBOT_QUEUE = 'sparertid_incoming'


class IMBot(object):
    _instance = None
    _commands = []

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(IMBot, cls).__new__(cls)

        return cls._instance

    def start(self):
        self.load_commands()

        self.connect_redis()
        self.connect_xmpp()
        self.xmpp_register_handlers()

        self.create_threads()

        self.loop()

    def loop(self):
        while not self.exit_event.is_set():
            try:
                self.xmpp_conn.Process(1)
            except KeyboardInterrupt:
                self.exit_event.set()

    def connect_redis(self):
        self.redis = redis.Redis(
            settings.REDIS_HOST,
            settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def create_threads(self):
        self.exit_event = threading.Event()

        def start_thread(target, args):
            t = threading.Thread(target=target, args=args)
            t.daemon = True
            t.start()

        args = (self.redis, self.exit_event, )
        for i in range(settings.IMBOT_THREADS):
            start_thread(IMBot.process_message, args)

    ############################################################################
    ## COMMANDS
    def load_commands(self):
        folder = os.path.join(os.path.dirname(__file__), 'commands')
        for name in os.listdir(folder):
            if name.startswith('__') or not name.endswith('.py'):
                continue

            module_name = name.rsplit('.', 1)[0]
            __import__('%s.commands.%s' % (__package__, module_name))

    @classmethod
    def command_register(cls, regex):
        def _command_register(func):
            cls._commands.append((re.compile(regex), func))
        return _command_register

    ############################################################################
    ## IM
    def connect_xmpp(self):
        jid = xmpp.JID(settings.IMBOT_JABBER_JID)
        user = jid.getNode()
        server = jid.getDomain()

        self.xmpp_conn = xmpp.Client(server, debug=[])
        connected = self.xmpp_conn.connect()
        if not connected:
            print 'unable to connect'
            sys.exit(1)

        authed = self.xmpp_conn.auth(user, settings.IMBOT_JABBER_PASSWORD)
        if not authed:
            print 'unable to auth'
            sys.exit(1)

        self.xmpp_conn.sendInitPresence()

    def xmpp_register_handlers(self):
        self.xmpp_conn.RegisterHandler('message', IMBot.xmpp_message_handler)

    @staticmethod
    def xmpp_message_handler(conn, message):
        if message.getType() in ('chat', 'normal'):
            IMBot().redis.rpush(
                IMBOT_QUEUE,
                json.dumps([
                    str(message.getFrom().getStripped()),
                    message.getBody()
                ])
            )

    @classmethod
    def send_message(cls, jid, text):
        msg = xmpp.Message(xmpp.JID(jid), text)
        cls().xmpp_conn.send(msg)

    @staticmethod
    def process_message(redis_conn, exit_event):
        User = get_user_model()

        while not exit_event.is_set():
            record = redis_conn.lpop(IMBOT_QUEUE)
            if record:
                jid, message = json.loads(record)
                try:
                    user = User.objects.get(jid=jid)
                except User.DoesNotExist:
                    IMBot.send_message(jid, _('user with this jid not found'))
                    continue

                timezone.activate(user.timezone)

                found = False
                for regex, func in IMBot._commands:
                    params = regex.search(message)
                    if params:
                        found = True
                        result = func(user, message, **params.groupdict())
                        if result:
                            IMBot.send_message(jid, result)
                        break

                if not found:
                    IMBot.send_message(jid, _(u'command not found'))
