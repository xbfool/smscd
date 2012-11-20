import web
import handler.handler
urls = (
    '/auth', 'handler.handler.handler'
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()