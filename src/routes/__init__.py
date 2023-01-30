import os

from ..controllers import get_images_by_id, search_by_name
from PyForgeAPI import Routes, Request, Response


DEBUG = False if not (_DEBUG := os.getenv("PORT")) else bool(_DEBUG)

routes = Routes(debug=DEBUG)


@routes.get("/search")
async def search(req: Request, res: Response):
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


@routes.get("/images/:manga_id")
async def images(req: Request, res: Response):
    manga_id = req.params.get("manga_id")

    if not manga_id:
        res.json(
            {
                "error": "BadRequest",
                "message": '"manga_id" parameter is required',
            }
        ).status(400).send()
        return

    try:
        manga_id = int(manga_id)
    except ValueError:
        res.json(
            {
                "error": "BadRequest",
                "message": '"manga_id" should be an integer',
            }
        ).status(400).send()
        return

    manga = None

    try:
        manga = get_images_by_id(manga_id)
    except RuntimeError as e:
        print(e)

        res.json(
            {
                "error": "NotFound",
                "message": f'"{manga_id}" not found',
            }
        ).status(404).send()
        return

    res.json({"data": manga}).status(200).send()
