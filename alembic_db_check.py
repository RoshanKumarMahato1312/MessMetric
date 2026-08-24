import sys
from sqlalchemy import create_engine, text

try:
    from app.config import settings
except Exception as e:
    print("IMPORT_SETTINGS_ERROR", type(e).__name__)
    sys.exit(2)

try:
    # Do NOT print the URL (sensitive). Use it only to connect.
    engine = create_engine(settings.DATABASE_URL)
except Exception as e:
    print("ENGINE_CREATION_ERROR", type(e).__name__)
    sys.exit(3)

try:
    with engine.connect() as conn:
        try:
            res = conn.execute(text("SELECT version_num FROM alembic_version"))
            rows = [r[0] for r in res]
            if rows:
                print("ALEMBIC_VERSION_TABLE_EXISTS")
                for v in rows:
                    print(v)
            else:
                print("ALEMBIC_VERSION_TABLE_EMPTY")
        except Exception as q_err:
            # If the table does not exist, we expect an exception such as UndefinedTableError.
            print("ALEMBIC_VERSION_QUERY_FAILED", type(q_err).__name__)
            sys.exit(4)
except Exception as conn_err:
    print("DB_CONNECTION_FAILED", type(conn_err).__name__)
    sys.exit(5)

sys.exit(0)
