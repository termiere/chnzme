from datetime import datetime, timedelta

from app.models.users import User
from app.models.user_words import UserWord
from app.models.words import Word


def test_review_new_word_again(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()
    word = Word(character="你好", pinyin="nǐ hǎo", hsk_level=1)

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
        json={
            "rating": "again",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "learning"
    assert data["learning_step"] == 0
    assert data["repetitions"] == 0
    assert data["interval"] == 0
    assert data["ease_factor"] == 2.5
    assert data["lapses"] == 0
    assert data["next_review"] is not None
    assert data["last_review"] is not None


def test_review_new_word_good_until_review(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()

    word = Word(character="谢谢", pinyin="xièxie", hsk_level=1)

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "learning"
    assert data["learning_step"] == 1
    assert data["repetitions"] == 0
    assert data["interval"] == 0

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "learning"
    assert data["learning_step"] == 2

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "review"
    assert data["learning_step"] == 0
    assert data["repetitions"] == 1
    assert data["interval"] == 1
    assert data["lapses"] == 0


def test_review_again_enters_relearning(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()

    word = Word(
        character="学习",
        pinyin="xuéxí",
        hsk_level=1,
    )

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
        status="review",
        repetitions=5,
        interval=10,
        ease_factor=2.5,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "again"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "relearning"
    assert data["learning_step"] == 0
    assert data["repetitions"] == 5
    assert data["interval"] == 10
    assert data["ease_factor"] == 2.5
    assert data["lapses"] == 1
    assert data["next_review"] is not None

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "relearning"
    assert data["learning_step"] == 1
    assert data["interval"] == 10
    assert data["lapses"] == 1

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "review"
    assert data["learning_step"] == 0
    assert data["repetitions"] == 6
    assert data["interval"] == 5
    assert data["lapses"] == 1


def test_review_good_increases_interval(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()

    word = Word(character="朋友", pinyin="péngyou", hsk_level=1)

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
        status="review",
        repetitions=3,
        interval=10,
        ease_factor=2.5,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "good"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "review"
    assert data["repetitions"] == 4
    assert data["interval"] == 25
    assert data["ease_factor"] == 2.5
    assert data["lapses"] == 0


def test_review_easy_increases_interval_faster(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()

    word = Word(character="工作", pinyin="gōngzuò", hsk_level=1)

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
        status="review",
        repetitions=3,
        interval=10,
        ease_factor=2.5,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "easy"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "review"
    assert data["repetitions"] == 4
    assert data["interval"] == 32
    assert data["ease_factor"] == 2.65
    assert data["lapses"] == 0


def test_review_easy_increases_interval_faster(client, auth_token, db_session):
    user = db_session.query(User).filter_by(username="hello").first()

    word = Word(character="工作", pinyin="gōngzuò", hsk_level=1)

    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)

    user_word = UserWord(
        user_id=user.id,
        word_id=word.id,
        status="review",
        repetitions=3,
        interval=10,
        ease_factor=2.5,
    )

    db_session.add(user_word)
    db_session.commit()

    response = client.post(
        f"/api/v1/user-words/{word.id}/review",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"rating": "easy"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "review"
    assert data["repetitions"] == 4
    assert data["interval"] == 32
    assert data["ease_factor"] == 2.65
    assert data["lapses"] == 0


def test_review_session_returns_due_words_before_new_words(
    client, db_session, auth_token
):
    due_word = Word(
        character="你好",
        pinyin="nǐ hǎo",
        hsk_level=1,
    )

    new_word_1 = Word(
        character="谢谢",
        pinyin="xiè xie",
        hsk_level=1,
    )

    new_word_2 = Word(
        character="学习",
        pinyin="xuéxí",
        hsk_level=1,
    )

    db_session.add_all(
        [
            due_word,
            new_word_1,
            new_word_2,
        ]
    )
    db_session.commit()

    due_user_word = UserWord(
        user_id=1,
        word_id=due_word.id,
        status="review",
        repetitions=3,
        interval=5,
        ease_factor=2.5,
        next_review=datetime.now() - timedelta(minutes=1),
    )

    new_user_word_1 = UserWord(
        user_id=1,
        word_id=new_word_1.id,
        status="new",
    )

    new_user_word_2 = UserWord(
        user_id=1,
        word_id=new_word_2.id,
        status="new",
    )

    db_session.add_all(
        [
            due_user_word,
            new_user_word_1,
            new_user_word_2,
        ]
    )
    db_session.commit()

    response = client.get(
        "/api/v1/user-words/review-session?limit=3",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    assert data[0]["word"]["character"] == "你好"
    assert data[0]["status"] == "review"

    assert data[1]["word"]["character"] == "谢谢"
    assert data[1]["status"] == "new"

    assert data[2]["word"]["character"] == "学习"
    assert data[2]["status"] == "new"
