#Front end takes things from back end
from enum import Enum
from typing import List
from pydantic import BaseModel
from pydantic import validator
from sqlalchemy.orm import Session
from dao.player_dao import Player


class PlayerSession:
    def __init__(self, session: Session, player: Player):
        self.session = session
        self.player = player


class LoginRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_can_not_be_blank(cls, v):
        assert v.strip(), "username can not be blank"
        return v

    @validator("password")
    def password_can_not_be_blank(cls, v):
        assert v.strip(), "password can not be blank"
        return v


class RegisterRequest(LoginRequest):
    pass


class Operator(str, Enum):
    ADD = "+",
    SUBTRACT = "-"


class CheckAnswerRequest(BaseModel):
    num1: int
    num2: int
    operator: Operator
    carry: List[int]
    answer: List[int]

    @validator("num1")
    def num1_must_be_2_digits(cls, v):
        assert 10 <= v <= 999, "num1 must be 3 digits"
        return v

    @validator("num2")
    def num2_must_be_2_digits(cls, v):
        assert 10 <= v <= 1000, "num2 must be 3 digits"
        return v

    @validator("carry")
    def carry_length_3(cls, v):
        assert len(v) == 3, "carry_length_3"
        return v

    @validator("answer")
    def answer_length_3(cls, v):
        assert len(v) == 3, "answer_length_3"
        return v
