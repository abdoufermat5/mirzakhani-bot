from db.dbConfig import OpenAIPrompt, Session
from sqlalchemy import desc

# get the session
session = Session()


def addRecord(question, answer, role):
    rec = OpenAIPrompt(question=question, answer=answer, answer_role=role)
    session.add(rec)
    session.commit()
    print("Record added")


def getLatestRecord():
    rec = session.query(OpenAIPrompt).order_by(OpenAIPrompt.id).first()
    session.close()

    return rec


def getAllRecords():
    rec = session.query(OpenAIPrompt).all()
    return rec


def getLastFiveRecords():
    # check if there's something in the db
    if session.query(OpenAIPrompt).count() == 0:
        return []
    rec = session.query(OpenAIPrompt).order_by(desc(OpenAIPrompt.id)).limit(5).all()
    return rec
