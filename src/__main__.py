import os
from .routes import routes

from dotenv import load_dotenv

load_dotenv()

PORT = 3000 if not (_PORT := os.getenv("PORT")) else int(_PORT)

routes.run(application="Manga API", host="localhost", port=PORT)
