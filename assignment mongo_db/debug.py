if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    from main import app

    app.root_path = None

import argparse
import gc
import logging

import uvicorn

from scripts.config import Service

gc.collect()

ap = argparse.ArgumentParser()

if __name__ == "__main__":
    ap.add_argument(
        "--port",
        "-p",
        required=False,
        default=Service.port,
        help="Port to start the application.",
    )
    ap.add_argument(
        "--bind",
        "-b",
        required=False,
        default=Service.host,
        help="IF to start the application.",
    )
    arguments = vars(ap.parse_args())

    logging.info(f"App Starting at {arguments['bind']}:{arguments['port']}")
    uvicorn.run("main:app", host=arguments["bind"], port=int(arguments["port"]))
