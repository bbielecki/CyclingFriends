from Users.DataAccess.users_db_context import db, engine, users

query = db.select([users])
result = engine.execute(query).fetchmany(size=10)

