# FAST API is the modern high performance api which is build on top of 2 main libraries starlette(request recives and reponse) and pydantic(Data validation)
# fast to code and run
# SGI(server gatway interface) -> convert https request to python understandable format and vice-versa.
# WEB_SERVER -> SGI -> API code
# flask has wsgi(synchronous)-> werkzeug(library) web_server(gunicorn)
# fast_api asgi(asynchronoud) -> stralette web_server (uvicorn)
# 