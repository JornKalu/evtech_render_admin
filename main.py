from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import sys, traceback

#Admin routes
from routers.admins.authentication import auth
from routers.admins.administrators import admins
from routers.admins.administrators import roles
from routers.admins.users import user
from routers.admins.batteries import battype
from routers.admins.batteries import batt
from routers.admins.stations import stata
from routers.admins.mob_devices import device_type
from routers.admins.mob_devices import device
from routers.admins.transaction import trans

# #Test routes
# from routers.tests import external

# Main app section here
app = FastAPI(title="EV Tech Admin")

#Admin routers
app.include_router(auth.router)
app.include_router(admins.router)
app.include_router(roles.router)
app.include_router(user.router)
app.include_router(battype.router)
app.include_router(batt.router)
app.include_router(stata.router)
app.include_router(device_type.router)
app.include_router(device.router)
app.include_router(trans.router)

# #Test routers
# app.include_router(external.router)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        return response
    except Exception as e:
        # err = "Stack Trace - %s \n" % (traceback.format_exc())
        err = traceback.print_exception(*sys.exc_info())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(err)}))


app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World! EV Tech Admin App"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, "url": request.base_url}),
    )

add_pagination(app)