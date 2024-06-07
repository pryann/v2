import subprocess
import sys
import uvicorn
from src.config import get_settings


settings = get_settings()


def dev():
    subprocess.run("fastapi dev ./src/main.py --reload")


def prod():
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.SERVER_LOG_LEVEL,
        timeout_keep_alive=settings.SERVER_TTL,
        ssl_keyfile=settings.SSL_KEYFILE,
        ssl_certfile=settings.SSL_CERTFILE,
    )


def alembic_init():
    subprocess.run(["alembic", "init", "alembic"], check=True)


def alembic_revision():
    message = sys.argv[1]
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)


def alembic_upgrade():
    subprocess.run(["alembic", "upgrade", "head"], check=True)


def alembic_downgrade():
    subprocess.run(["alembic", "downgrade", "base"], check=True)
