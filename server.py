import web
import json

uid = 1
app = web.application(('/', 'index'), globals())

class index(object):
    counter = 0
    def GET(self):
        self.__class__.counter += 1
        return json.dumps(
            {
                'count': self.__class__.counter,
                'uid': uid
                }
            )

if __name__ == "__main__":
    app.run()
