from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    return {"message": "CICD with git action to AWS EC2"}