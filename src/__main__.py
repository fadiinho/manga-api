import os
from dotenv import load_dotenv

load_dotenv()

from PyForgeAPI import Routes, Response, Request

from .controllers import search_by_name

# Using `.cors()` until it gets fixed on the package
routes = Routes(debug=True).cors()


@routes.get("/")
async def home(req: Request, res: Response):
    search_term = req.query.get("search_term")
    if not search_term:
        res.json(
            {
                "error": "BadRequest",
                "message": '"search_term" parameter is required',
            }
        ).status(400).send()
        return

    result = search_by_name(search_term)

    if not result:
        res.json(
            {
                "error": "NotFound",
                "message": f"`'{search_term}' not found",
            }
        ).status(404).send()
        return

    res.json({"result": result}).status(200).send()


PORT = 3000 if not (_PORT := os.getenv("PORT")) else int(_PORT)

routes.run(application="Person API", host="localhost", port=PORT)
