from database import get_session

session = get_session()

result = session.run("MATCH (n) RETURN n LIMIT 5")

for record in result:
    print(record)