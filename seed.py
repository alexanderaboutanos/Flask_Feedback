from app import db
from models import User, Feedback

db.drop_all()
db.create_all()

user1 = User.register(username="Coolkids1", password='cool',
                      email='coolkid123@aol.com', first_name='James', last_name='Beb')
user2 = User.register(username="Coolkids2", password='cool',
                      email='coolkid1234@aol.com', first_name='Lindsey', last_name='Lohan')
user3 = User.register(username="Coolkids3", password='cool',
                      email='coolkid1235@aol.com', first_name='Kelly', last_name='Slater')


db.session.add_all([user1, user2, user3])
db.session.commit()

feedback1 = Feedback(
    title='Skating', content='Had a sweet skate sesh today. Till next time!', username='Coolkids1')
feedback2 = Feedback(
    title='Surfing', content='Waves were all chop today, no barrel whatsoever. dissapointing...', username='Coolkids2')
feedback3 = Feedback(
    title='Jammin', content='got together with the boyz for a rippin jam session today. 10/10!', username='Coolkids3')

db.session.add_all([feedback1, feedback2, feedback3])
db.session.commit()
