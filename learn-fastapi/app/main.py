from fastapi import FastAPI, Query
from services.products import load_products

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/products")
async def read_item(name: str=Query(None, min_length=3, max_length=50, description="Name of the product to search for")):
    products = await load_products()
    return {"products": products}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)