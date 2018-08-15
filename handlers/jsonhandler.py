import tornado.escape
import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class JsonHandler(BaseHandler):
    def prepare(self):
        if self.request.body:
            try:
                # print(self.request.body)
                # для дебага через curl
                arg = self.request.body
                arg = arg.decode()
                arg = arg.replace("'", '"')

                self.json_data = tornado.escape.json_decode(arg)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)