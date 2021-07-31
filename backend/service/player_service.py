#This part is for logic of our player game rules
#To acheive actual function, we need to adjust player_dao's method
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import db
from dao.player_dao import Player
import uuid
from dto.request_dto import Operator, CheckAnswerRequest
from dto.response_dto import InfoResponse
from dto.exception_dto import MathException


def login(username: str, password: str) -> str:
    session = db.connect()
    query = session.query(Player).filter_by(username=username, password=password)
    assert query.count() == 1, "player not exists or password wrong!"
    player = query.one()
    token = str(uuid.uuid4())
    player.token = token
    session.commit()
    session.close()
    return token


def logout(session: Session, player: Player) -> bool:
    player.token = None
    session.commit()
    session.close()
    return True


def info(session: Session, player: Player) -> InfoResponse:
    player.token = None
    res = InfoResponse(username=player.username, score=player.score)
    session.close()
    return res


def register(username: str, password: str) -> bool:
    session = db.connect()
    player = Player(username=username, password=password)
    session.add(player)
    try:
        session.commit()
        session.close()
    except IntegrityError:
        raise AssertionError("username exists")
    return True


def unregister(username:str, password:str) -> bool:
    session = db.connect()
    query = session.query(Player).filter_by(username=username, password=password)
    count = query.count()
    assert count == 1, "username not found or password wrong!"
    player = query.one()
    session.delete(player)
    session.commit()
    session.close()
    return True


def add_score(session: Session, player: Player, amount: int) -> int:
    player.score = Player.score + amount
    return player.score


def minus_score(session: Session, player: Player, amount: int) -> int:
    if(player.score>0):
        player.score = Player.score - amount
    else:
        player.score = 0
    return player.score


def clear_score(session: Session, player: Player) -> int:
    player.score = 0
    session.commit()
    session.close()
    return player.score


def submit(session: Session, player: Player,
           args: CheckAnswerRequest) -> bool:
    try:
        correct = check_answer(**args.dict())
        add_score(session, player, 1)
        session.commit()
        session.close()
    except MathException as e:
        minus_score(session, player, 1)
        session.commit()
        session.close()
        raise e
    return correct

def check_answer(num1: int, num2: int, operator: Operator,
                 carry: List[int], answer: List[int]):
    expected = answer[0] * 100 + answer[1] * 10 + answer[2]
    if operator is Operator.ADD:
        actual = num1 + num2
        if expected != actual:
            raise MathException("Expected: {}, Actual: {}".format(expected, actual))

        expected_carry = [(num1//10 + num2//10 + carry[1])//10, (num1%10 + num2%10)//10, 0]
        if carry[2] != expected_carry[2]:
            raise MathException("The first carry should always be 0")
        if carry[1] != expected_carry[1]:
            raise MathException("The second carry should be {}".format(expected_carry[1]))
        if carry[0] != expected_carry[0]:
            raise MathException("The third carry should be {}".format(expected_carry[0]))
            return True
    elif operator is Operator.SUBTRACT:
        actual = num1 - num2

        if expected != actual:
            raise MathException("Expected: {}, Actual: {}".format(expected, actual))
        expected_middle = 0
        if num1%10 < num2%10:
            expected_middle = -1
        expected_left = 0
        if num1%100 < num2%100:
            expected_left = -1
        expected_carry = [expected_left, expected_middle, 0]
        if carry[2] != expected_carry[2]:
            raise MathException("The first carry should always be 0")
        if carry[1] != expected_carry[1]:
            raise MathException("The second carry should be {}".format(expected_carry[1]))
        if carry[0] != expected_carry[0]:
            raise MathException("The third carry should be {}".format(expected_carry[0]))
        return True
        
    else:
        raise MathException("Unknown Error")


