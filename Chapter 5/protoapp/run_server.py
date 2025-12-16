import uvicorn 
# from proto_app.main import app

if __name__ == "__main__":
    uvicorn.run("proto_app.main:app", reload=True)

