from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from routes.events import event_router
from routes.users import user_router


app = FastAPI()
app.include_router(event_router)
app.include_router(user_router)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc:RequestValidationError):
    return JSONResponse(
        status_code =400,
        content = jsonable_encoder({'code': '400', 'message':'Invalid Entry'}))



# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc: RequestValidationError):
#     message = "Validation errors:"
#     for error in exc.errors():
#         message += f"\nField: {error['loc']}, Error: {error['msg']}"
#     return PlainTextResponse(message, status_code=400)
  