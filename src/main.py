from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.connections.base import BaseConnection
from src.routes.patients import router as patients_router
from src.routes.appointments import router as appointments_router

app = FastAPI()

app.include_router(patients_router)
app.include_router(appointments_router)


# can be used to check if the database is up when deployed
@app.get(
    "/api/status",
    summary="Check the status of the database",
    description="Returns the status of the database.",
    response_description="The status of the database.",
    tags=["status"],
    responses={
        200: {
            "description": "The status of the database.",
            "content": {"application/json": {"example": {"status": "ok", "db": "up"}}},
        },
        503: {
            "description": "The status of the database.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "db": "down",
                        "detail": "Connection to database failed",
                    }
                }
            },
        },
    },
)
def health_check():
    base_connection = BaseConnection()
    db_status = base_connection.health_check()
    if db_status == 1:
        return JSONResponse(
            content={"status": "ok", "db": "up"}, status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={
                "status": "error",
                "db": "down",
                "detail": "Connection to database failed",
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
