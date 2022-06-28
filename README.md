# DATADOG Flask poc

```bash
# Dev
$ DD_API_KEY=xxx FLASK_DEBUG=1 FLASK_ENV="dev" docker-compose up -d
# PROD
$ DD_API_KEY=xxx FLASK_DEBUG=0 FLASK_ENV="production" docker-compose up -d
```

Call Endpoints
```bash
$ curl http://localhost
{
  "APPLICATION_ROOT": "/", 
  "DEBUG": "0", 
  "ENV": "production", 
  "EXPLAIN_TEMPLATE_LOADING": "False", 
  "JSONIFY_MIMETYPE": "application/json", 
  "JSONIFY_PRETTYPRINT_REGULAR": "False", 
  "JSON_AS_ASCII": "True", 
  "JSON_SORT_KEYS": "True", 
  "MAX_CONTENT_LENGTH": "None", 
  "MAX_COOKIE_SIZE": "4093", 
  "PERMANENT_SESSION_LIFETIME": "31 days, 0:00:00", 
  "PREFERRED_URL_SCHEME": "http", 
  "PRESERVE_CONTEXT_ON_EXCEPTION": "None", 
  "PROPAGATE_EXCEPTIONS": "None", 
  "SECRET_KEY": "None", 
  "SEND_FILE_MAX_AGE_DEFAULT": "None", 
  "SERVER_NAME": "None", 
  "SESSION_COOKIE_DOMAIN": "None", 
  "SESSION_COOKIE_HTTPONLY": "True", 
  "SESSION_COOKIE_NAME": "session", 
  "SESSION_COOKIE_PATH": "None", 
  "SESSION_COOKIE_SAMESITE": "None", 
  "SESSION_COOKIE_SECURE": "False", 
  "SESSION_REFRESH_EACH_REQUEST": "True", 
  "TEMPLATES_AUTO_RELOAD": "None", 
  "TESTING": "False", 
  "TRAP_BAD_REQUEST_ERRORS": "None", 
  "TRAP_HTTP_EXCEPTIONS": "False", 
  "USE_X_SENDFILE": "False"
}

$ curl http://localhost/abort
<html>
  <head>
    <title>Internal Server Error</title>
  </head>
  <body>
    <h1><p>Internal Server Error</p></h1>
    
  </body>
</html>

$ curl http://localhost/raise
<html>
  <head>
    <title>Internal Server Error</title>
  </head>
  <body>
    <h1><p>Internal Server Error</p></h1>
    
  </body>
</html>
$ docker-compose down --remove-orphans
```