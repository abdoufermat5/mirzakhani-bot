from db.dbConfig import OpenAIPrompt, Session, DirectChat
from sqlalchemy import desc

# get the session
session = Session()


def addRecord(question, answer, role=None, type=1):
    if type == 1:
        rec = OpenAIPrompt(question=question, answer=answer, answer_role=role)
    else:
        rec = DirectChat(question=question, answer=answer)
    session.add(rec)
    session.commit()
    print("Record added")


def getLatestRecord(type=1):
    if type == 1:
        rec = session.query(OpenAIPrompt).order_by(OpenAIPrompt.id).first()
    else:
        rec = session.query(DirectChat).order_by(DirectChat.id).first()
    session.close()

    return rec


def getAllRecords(type=1):
    if type == 1:
        rec = session.query(OpenAIPrompt).all()
    else:
        rec = session.query(DirectChat).all()
    return rec


def getLastFiveRecords(type=1):
    if type == 1:
        # check if there's something in the db
        if session.query(OpenAIPrompt).count() == 0:
            return []
        rec = session.query(OpenAIPrompt).order_by(desc(OpenAIPrompt.id)).limit(5).all()
    else:
        # check if there's something in the db
        if session.query(DirectChat).count() == 0:
            return []
        rec = session.query(DirectChat).order_by(desc(DirectChat.id)).limit(5).all()
    return rec
