from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def display_images(request: Request):

    # Step 1: Download the JSON payload
    url = "https://dss-hydra-feeds-prod.bamgrid.com/samsung/us/strands/curatedstrand.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        json_payload = response.json()

    # Step 2: Parse the title and image URL from the payload
    sections = json_payload.get("sections", [])
    images = []
    for section in sections:
        tiles = section.get("tiles", [])
        for tile in tiles:
            title = tile.get("title", "")
            image_url = tile.get("image_url", "")
            images.append({"title": title, "image_url": image_url})

    # Step 3: Render the HTML template with the images
    return templates.TemplateResponse("index.html", {"request": request, "images": images})


@app.on_event("shutdown")
async def shutdown_event():
    # Add any cleanup or shutdown tasks here
    print("Shutting down the server...")


if __name__ == "__main__":
    import uvicorn

    try:
        loop = asyncio.get_event_loop()
        loop.set_task_factory(lambda loop, coro: asyncio.Task(coro, name=str(id(coro))))
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        loop.stop()
