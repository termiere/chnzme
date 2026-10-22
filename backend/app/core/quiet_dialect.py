from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg
from sqlalchemy.dialects import registry
from sqlalchemy.engine import make_url
import psycopg

from app.core.config import settings


class QuietDialect(PGDialect_psycopg):
    supports_statement_cache = True

    def initialize(self, connection):
        self.server_version_info = (17, 11)
        self._backslash_escapes = False
        self.supports_native_enum = True
        self.supports_smallserial = True
        self._has_native_hstore = False


registry.register("postgresql.quiet", __name__, "QuietDialect")


def get_engine():
    u = make_url(settings.DATABASE_URL)

    def creator():
        return psycopg.connect(
            host=u.host,
            port=u.port,
            dbname=u.database,
            user=u.username,
            password=u.password,
            sslmode="require",
            connect_timeout=15,
            prepare_threshold=None,
        )

    return create_engine(
        "postgresql+quiet://",
        creator=creator,
        poolclass=NullPool,
        pool_pre_ping=True,
    )
