from sqlalchemy import create_engine


def main():
    engine = create_engine('sqlite:///db/blogs.db')
    with engine.connect() as con:
        con.execute("ALTER TABLE news ADD COLUMN address text")
        con.execute("ALTER TABLE news ADD COLUMN latitude float")
        con.execute("ALTER TABLE news ADD COLUMN longitude float")


if __name__ == "__main__":
    main()
