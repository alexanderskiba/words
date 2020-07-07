from sqlalchemy import create_engine

user = 'postgres'
passwd = '31471'
cur_string = f"postgresql://{user}:{passwd}@127.0.0.1:5432/eng_words"
cur = create_engine(cur_string)

# cur.execute("DROP TABLE IF EXISTS learning")
cur.execute("CREATE TABLE IF NOT EXISTS learning (ID SERIAL PRIMARY KEY, Word varchar(255), Translate varchar(255), DeckID varchar(255))")
for i in range(10):

    cur.execute("INSERT INTO learning (Word, Translate, DeckID) VALUES ('dog','собака','1')")

result = cur.execute("SELECT * FROM learning")

for i in result:
    print(i)

