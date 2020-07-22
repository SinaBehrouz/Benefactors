from flask.cli import FlaskGroup
from benefactors import app, db

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    from benefactors.models import User, Post
    users = []
    #the password is 123123123 ,use that to login
    users.append(User(username="sina", first_name="si", last_name="na", email="1@1.com", phone_number="1111", postal_code="111", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    users.append(User(username="Arian", first_name="Ari", last_name="an", email="2@2.com", phone_number="1111", postal_code="111", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    posts = []
    posts.append(Post(title="Gond with the Windds", description="A shitty book", user_id=1))
    posts.append(Post(title="CMPT-470 textbook", description="A ok book", user_id=1))
    posts.append(Post(title="CMPT-454 textbook", description="A shitty cmpt book", user_id=1))
    posts.append(Post(title="Physics", description="A supershitty book", user_id=2))
    posts.append(Post(title="idk anymoref", description="wtf", user_id=2))

    for i in users:
        db.session.add(i)
    for i in posts:
        db.session.add(i)

    db.session.commit()

if __name__ == "__main__":
    cli()
