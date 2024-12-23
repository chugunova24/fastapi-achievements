from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.enums.languages import LanguageEnum
from app.models.user import User, UserAchievement
from app.models.achievement import Achievement


def init_db(db: Session):
    # Проверим, существуют ли уже данные
    if not db.query(User).first():
        # Создание начальных пользователей
        user1 = User(name="John", language=LanguageEnum.EN)
        user2 = User(name="Maria", language=LanguageEnum.EN)
        user3 = User(name="Alice", language=LanguageEnum.RU)
        db.add(user1)
        db.add(user2)
        db.add(user3)

    if not db.query(Achievement).first():
        # Создание начальных достижений
        achievement1 = Achievement(
            name_en="I fucked it all",
            name_ru="В рот это все",
            points=10,
            description_en="Sorry, I won't come to school...no, no...I'm not sick...I just...",
            description_ru="изивините я не приду на учебу...неь нет...я не заболел... я просто...",
        )
        achievement2 = Achievement(
            name_en="Guys, I woke up at 5 pm.",
            name_ru="РЕбят я проснулся в 5 часов вечера",
            points=100,
            description_en="Sleep after hard work",
            description_ru="Работяжный сон",
        )
        achievement3 = Achievement(
            name_en="from $900 to $19.81",
            name_ru="от 900руб к 19.81руб",
            points=30,
            description_en="where's my money lebowski",
            description_ru="где мои деньги лебовски",
        )
        achievement4 = Achievement(
            name_en="The unhappy boss",
            name_ru="босс не доволен",
            points=40,
            description_en="unhappy about something there",
            description_ru="чем-то не доволен там",
        )
        achievement5 = Achievement(
            name_en="Next year i will up..",
            name_ru="В следующем году я повышу",
            points=60,
            description_en="my stupidity level",
            description_ru="свой уровень глупенькости",
        )
        achievement6 = Achievement(
            name_en="I am normal",
            name_ru="Я нормальный",
            points=150,
            description_en="and can be trusted to work from home",
            description_ru="и мне можно доверить работу из дома правда правда",
        )
        achievement7 = Achievement(
            name_en="With rude people online",
            name_ru="С грубиянами в сети",
            points=70,
            description_en="we need to go out one on one and smash a bottle on his uh face and drown him in a ditch so he dies, you freak",
            description_ru="надо выходить один на один и разбить бутылку об его эээ рожу и утопить в э вканаве чтоб он сдох урод",
        )
        db.add(achievement1)
        db.add(achievement2)
        db.add(achievement3)
        db.add(achievement4)
        db.add(achievement5)
        db.add(achievement6)
        db.add(achievement7)

        # назначение достижений пользователям
        db.add(UserAchievement(user_id=1,
                               achievement_id=1,
                               issued_at=datetime.now() + timedelta(days=1)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=2,
                               issued_at=datetime.now() - timedelta(days=2)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=3,
                               issued_at=datetime.now() - timedelta(days=3)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=4,
                               issued_at=datetime.now() - timedelta(days=4)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=5,
                               issued_at=datetime.now() - timedelta(days=5)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=6,
                               issued_at=datetime.now() - timedelta(days=6)))
        db.add(UserAchievement(user_id=1,
                               achievement_id=7,
                               issued_at=datetime.now() - timedelta(days=7)))

        db.add(UserAchievement(user_id=2, achievement_id=2))
        db.add(UserAchievement(user_id=3, achievement_id=3))

    db.commit()
