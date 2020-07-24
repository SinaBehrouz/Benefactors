from flask.cli import FlaskGroup
from benefactors import app, db
from benefactors.models import User, Post, PostComment

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    #user: 1@1.com
    #password: 123123123
    
    db.session.add(User(id =0, username="NULL", first_name="NULL", last_name="NULL", email="NULL", phone_number="NULL", postal_code="NULL", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="sina", first_name="si", last_name="na", email="1@1.com", phone_number="1111", postal_code="111", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="Arian", first_name="Ari", last_name="an", email="2@2.com", phone_number="1111", postal_code="111", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))

    db.session.add(Post(title="Tesla", description="A car company", user_id=1))
    db.session.add(Post(title="CMPT-470 textbook", description="John Leak (c. 1892 – 1972) was an Australian recipient of the Victoria Cross, the highest award for gallantry in battle that could be awarded at that time to a member of the Australian armed forces. Leak enlisted in early 1915, and served with the 9th Battalion during the Gallipoli campaign. Along with his unit, he transferred to the Western Front, where he participated in the Battle of Pozières in July 1916. For his actions on 23 July during this battle he was awarded the Victoria Cross. He was seriously wounded at the Battle of Mouquet Farm in August. Suffering from the effects of his service, Leak was convicted of desertion in November 1917, but his sentence was ultimately suspended. In early March 1918 he was gassed, and saw no further combat before the Armistice of 11 November 1918. He returned to Australia and was discharged in 1919. After various jobs, Leak settled in South Australia in 1937 and died in 1972", user_id=1))
    db.session.add(Post(title="CMPT-454 textbook", description="A CMPT book", user_id=2))
    db.session.add(Post(title="Physics", description="A Book", user_id=2))
    db.session.add(Post(title="SpaceX", description="A space exploration company", user_id=1))

    db.session.commit()

    db.session.add(PostComment(comment_desc = "This is a hello test comment from create DB", user_id=1, post_id = 2))
    db.session.add(PostComment(comment_desc = "This is the second comment", user_id=1, post_id = 2))

    db.session.commit()


if __name__ == "__main__":
    cli()

