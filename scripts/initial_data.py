from sqlalchemy.orm import Session
from apps.app.models import App
from apps.user.models import User
from apps.event.models import Event
from apps.story.models import Story

from fastapi import Depends
from core.database import get_db

def create_initial_data(db: Session = Depends(get_db)):
    db.query(Event).delete()
    db.query(User).delete()
    db.query(Story).delete()
    db.query(App).delete()
    
    records = []
    for i in range(1,4):
        records.append(App(id=i, token=f"token{i}"))
    db.add_all(records)
    db.commit()

    story1 = Story(story_id=1, app_id=1, metadata_={"img": "image1.png"})
    story2 = Story(story_id=2, app_id=1, metadata_={"img": "image2.png"})
    story3 = Story(story_id=3, app_id=1, metadata_={"img": "image3.png"})
    story4 = Story(story_id=4, app_id=2, metadata_={"img": "image4.png"})
    story5 = Story(story_id=5, app_id=3, metadata_={"img": "image5.png"})
    story6 = Story(story_id=6, app_id=3, metadata_={"img": "image6.png"})
    story7 = Story(story_id=7, app_id=3, metadata_={"img": "image7.png"})
    story8 = Story(story_id=8, app_id=3, metadata_={"img": "image8.png"})

    records = []
    for i in range(1,4):
        records.append(User(id=i, name=f"user{i}", mail=f"user{i}@gmail.com"))
    db.add_all(records)
    db.commit()
    
    db.add_all([story1, story2, story3, story4, story5, story6, story7, story8])
    db.commit()

    # you can open pgadmin and run the commands for adding events records
    # INSERT INTO public.events(
	# app_id, story_id, user_id, date, type, count)
	# VALUES (1, 1, 24, '2023-12-24', 'impression', 2),
	#  		(1, 1, 25, '2023-12-24', 'impression', 4);