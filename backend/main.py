#Main function is to define ports of connection
from fastapi import FastAPI, Depends, Request, status, Header
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import db
from dao.player_dao import Player
from dto.request_dto import LoginRequest, RegisterRequest, CheckAnswerRequest, PlayerSession
from dto.exception_dto import MathException
from service import player_service
import uvicorn

app = FastAPI()

# solve CORS problem
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_player_from_token(token: str = Header(...,)) -> PlayerSession:
    session = db.connect()
    query = session.query(Player).filter_by(token=token)
    if query.count() != 1:
        raise HTTPException(
            status_code=401,
            detail="invalid token!"
        )
    session.close()
    return PlayerSession(session, query.one())


@app.exception_handler(MathException)
async def exception_handler(request: Request, exc: MathException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 0, "data": str(exc)})
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = ';'.join([e["msg"]+":"+str(e["loc"]) for e in exc.errors()])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 0, "data": message})
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"code": 0, "data": exc.detail})
    )


@app.exception_handler(AssertionError)
async def assert_exception_handler(request: Request, exc: AssertionError):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 0, "data": str(exc)})
    )


@app.post("/login")
async def login(args: LoginRequest):
    result = player_service.login(**args.dict())
    return {"code": 1, "data": result}

#Depence is used for intercepting, if you haven't logged out, you will be stopped 
@app.post("/logout")
async def logout(ps: PlayerSession = Depends(get_player_from_token)):
    result = player_service.logout(ps.session, ps.player)
    return {"code": 1, "data": result}


@app.post("/register")
async def register(args: RegisterRequest):
    result = player_service.register(**args.dict())
    return {"code": 1, "data": result}


@app.post("/unregister")
async def unregister(args: RegisterRequest):
    result = player_service.unregister(args.username, args.password)
    return {"code": 1, "data": result}


@app.post("/submit")
async def submit(args: CheckAnswerRequest, ps: PlayerSession = Depends(get_player_from_token)):
    result = player_service.submit(ps.session, ps.player, args)
    return {"code": 1, "data": result}

@app.post("/submit2")
async def submit2(args: CheckAnswerRequest, ps: PlayerSession = Depends(get_player_from_token)):
    result = player_service.submit2(ps.session, ps.player, args)
    return {"code": 1, "data": result}


@app.post("/clear")
async def check(ps: PlayerSession = Depends(get_player_from_token)):
    result = player_service.clear_score(ps.session, ps.player)
    return {"code": 1, "data": result}


@app.post("/info")
async def info(ps: PlayerSession = Depends(get_player_from_token)):
    result = player_service.info(ps.session, ps.player)
    return {"code": 1, "data": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
