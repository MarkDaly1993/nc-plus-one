from fastapi import FastAPI
from db.routes.events import event_router
app = FastAPI()
app.include_router(event_router)




  