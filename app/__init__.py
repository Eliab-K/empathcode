from fastapi import FastAPI
<<<<<<< HEAD
from app.main import router
=======
#from app.main import router
>>>>>>> master
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Mount all routes from main.py
<<<<<<< HEAD
app.include_router(router)
=======
#app.include_router(router)
>>>>>>> master

# Enable session management (for login)
app.add_middleware(SessionMiddleware, secret_key="supersecret")  

# Re-export the app for deployment tools
application = app
