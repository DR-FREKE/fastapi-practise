from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Error.customerror import CustomError

app2 = FastAPI()


@app2.exception_handler(CustomError)
async def errorHandler(req: Request, err: CustomError):
    if isinstance(err, CustomError):
        return JSONResponse(status_code=err.statusCode, content={"error": err.serializeError()})
