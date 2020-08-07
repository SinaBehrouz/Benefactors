from flask.cli import FlaskGroup
from benefactors import app, db
from benefactors.models import User, Post, PostComment, ChatChannel, ChatMessages

import datetime

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # user: 1@1.com
    # password: 123123123

    db.session.add(User(id =0, username="NULL", first_name="NULL", last_name="NULL", email="NULL", phone_number="NULL", postal_code="NULL", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="sina123", first_name="Sina", last_name="Smith", email="1@1.com", phone_number="1111", postal_code="V3E3B5", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="Arian123", first_name="Arian", last_name="Smith", email="2@2.com", phone_number="1111", postal_code="V5Z0G7", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="Martin777", first_name="Martin", last_name="Jo", email="3@3.com", phone_number="12345", postal_code="V5Z0G7", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="Simran122", first_name="Simran", last_name="Gulati", email="4@4.com", phone_number="54231", postal_code="V3Z4B2", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))
    db.session.add(User(username="Hansen99", first_name="Hansen", last_name="William", email="5@5.com", phone_number="54321", postal_code="V3Z4B2", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y"))

    db.session.add(Post(title="Clean Tesla", category="GROCERY", description="Really need help cleaning my Tesla. You can take it for a ride at the end.", user_id=1))
    db.session.add(Post(title="Need a Book, Ideally Like the One in the Description", category="GROCERY", description="John Leak (c. 1892 – 1972) was an Australian recipient of the Victoria Cross, the highest award for gallantry in battle that could be awarded at that time to a member of the Australian armed forces. Leak enlisted in early 1915, and served with the 9th Battalion during the Gallipoli campaign. Along with his unit, he transferred to the Western Front, where he participated in the Battle of Pozières in July 1916. For his actions on 23 July during this battle he was awarded the Victoria Cross. He was seriously wounded at the Battle of Mouquet Farm in August. Suffering from the effects of his service, Leak was convicted of desertion in November 1917, but his sentence was ultimately suspended. In early March 1918 he was gassed, and saw no further combat before the Armistice of 11 November 1918. He returned to Australia and was discharged in 1919. After various jobs, Leak settled in South Australia in 1937 and died in 1972", user_id=1))
    db.session.add(Post(title="Please Help Get My Groceires", category="GROCERY", description="Would really appreciate someone picking up some essential groceries. Eggs, bread, milk, that kind of thing.", user_id=2, volunteer=1))
    db.session.add(Post(title="Need to Get My Medications", category="GROCERY", description="I'm a little scared to step out to get meds from my local pharmacy, would really appreciate if someone could pick them up for me", user_id=2, volunteer=1))
    db.session.add(Post(title="SpaceX, Hire me", category="GROCERY", description="Elon, if you see this, hire me.", user_id=1))

    db.session.commit()

    db.session.add(PostComment(comment_desc="Thappis is a hello test comment from create DB", user_id=1, post_id=2))
    db.session.add(PostComment(comment_desc="This is the second comment", user_id=1, post_id=2))

    db.session.add(ChatChannel(user1_id=1, user2_id=3, last_updated = datetime.datetime(2020, 7, 19, 12, 5, 30)))
    db.session.add(ChatChannel(user1_id=2, user2_id=3, last_updated = datetime.datetime(2020, 7, 25, 12, 5, 30)))
    db.session.add(ChatChannel(user1_id=3, user2_id=4, last_updated = datetime.datetime(2020, 7, 21, 12, 5, 30)))
    db.session.add(ChatChannel(user1_id=3, user2_id=5, last_updated = datetime.datetime(2020, 7, 20, 12, 5, 30)))
    
    db.session.commit()
    
    db.session.add(ChatMessages(sender_id=1, message_content="Test message bruh", channel_id=1, message_time = datetime.datetime(2020, 7, 20, 12, 5, 30)))
    db.session.add(ChatMessages(sender_id=3, message_content="Test message received bruh", channel_id=1, message_time = datetime.datetime(2020, 7, 20, 13, 6, 30)))
    
    db.session.add(ChatMessages(sender_id=1, message_content="Test message bruh 2", channel_id=1, message_time = datetime.datetime(2020, 7, 20, 14, 5, 30)))
    db.session.add(ChatMessages(sender_id=3, message_content="Test message received bruh 2", channel_id=1, message_time = datetime.datetime(2020, 7, 20, 15, 5, 30)))
    
    db.session.add(ChatMessages(sender_id=1, message_content="Test message bruh 3", channel_id=1, message_time = datetime.datetime(2020, 7, 20, 16, 5, 30)))
    db.session.add(ChatMessages(sender_id=3, message_content="Test message received bruh 3" , channel_id=1, message_time = datetime.datetime(2020, 7, 20, 17, 5, 30)))

    db.session.commit()


if __name__ == "__main__":
    cli()
