from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from routes.events import event_router
from routes.authenticate import authenticate_router
# from routes.rsvps import rsvp_router





app = FastAPI()
app.include_router(event_router)
app.include_router(authenticate_router)
# app.include_router(rsvp_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc:RequestValidationError):
    return JSONResponse(
        status_code =400,
        content = jsonable_encoder({'code': '400', 'message':'Invalid Entry'}))

