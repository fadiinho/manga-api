import os

from ..controllers import search_by_name
from PyForgeAPI import Routes, Request, Response

DEBUG = False if not (_DEBUG := os.getenv("PORT")) else bool(_DEBUG)

routes = Routes(debug=DEBUG)


@routes.get("/search")
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
