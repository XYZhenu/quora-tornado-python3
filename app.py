# coding: UTF-8
import os
import re
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import unicodedata
from tornado.options import define, options
from jinja2 import Template, Environment, FileSystemLoader
from handlers import *
import filter
import session
from mongoengine import *

def markdown_tag(str):
    return filter.markdown.markdown(str)

define("port", default=18888, help="run on the given port", type=int)
define("mongo_host", default="127.0.0.1:27017", help="database host")
define("mongo_database", default="quora", help="database name")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/login", LoginHandler),
            (r"/register", RegisterHandler),
            (r"/logout", LogoutHandler),
            (r"/ask/([^/]+)", AskShowHandler),
            (r"/feed", FeedHandler),
            (r"/ask/([^/]+)/answer", AnswerHandler),
            (r"/ask/([^/]+)/flag", FlagAskHandler),
            (r"/ask", AskHandler),
            (r"/answer/([^/]+)/vote", AnswerVoteHandler),
            (r"/comment/([^/]+)/([^/]+)", CommentHandler),
            (r"/ask", AskHandler),
            (r"/settings", SettingsHandler),
            (r"/([^/]+)", ProfileHandler),
        ]
        settings = dict(
            app_name=u"我知",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="81o0TzKaPpGtYdkL5gEmGepeuuYi7EPnp2XdTP1o&Vo=",
            login_url="/login",
            session_secret='08091287&^(01',
            session_dir=os.path.join(os.path.dirname(__file__), "tmp/session"),
        )
        self.session_manager = session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])
        tornado.web.Application.__init__(self, handlers, **settings)

        # Connection MongoDB
        connect(options.mongo_database)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == "__main__":
    main()
