from fastapi import APIRouter, File, UploadFile, Depends
from app.response import BaseResponse
from sqlalchemy.orm import Session
from app.response import CommonResponse
from scoreRecognition.scoreRecognition import recognition
import scoreRecognition.createOutput as co
import scoreRecognition.upload as up
from app import database

import os

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

rScore = APIRouter(prefix="/py-api/score")

@rScore.post('/', tags = ['score'], response_model=BaseResponse)
def upload_score(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if(file == None): # 파일을 전송받지 못한 경우
        return CommonResponse(False, None, 400, "파일 업로드에 실패했습니다. 다시 시도해주세요.")
    
    if(file.content_type != "application/pdf"): # 지원하지 않는 파일 형식
        return CommonResponse(False, None, 400, f"{file.content_type.split('/')[1]} 파일 형식을 지원하지 않습니다.")
    
    recognition(file, db)
    
    return CommonResponse(
        True,
        {
            "filename": file.filename,
            "content_type": file.content_type,
            "messgae": f"{file.content_type.split('/')[1]} 형식의 파일이 업로드 되었습니다."
        },
        200, "파일 전송 성공!"
        )

@rScore.get('/{team_id}', tags = ['score'], response_model=BaseResponse)
def get_scores(team_id: int, db: Session = Depends(get_db)):
    scoreData = db.query(Score.score_url, Accompainment.accompainment_url, Position.position_name, Color.color_code)\
        .join(Accompainment, Score.score_id == Accompainment.score_id)\
        .join(Position, Score.position_id == Position.position_id)\
        .join(Color, Position.color_id == Color.color_id)\
        .filter(Score.team_id==team_id)\
        .all()
    
    return CommonResponse(
        True,
        scoreData,
        200, "조회 성공!"
        )

@rScore.delete('/{team_id}', tags = ['score'], response_model=BaseResponse)
def delete_scores(team_id: int, db: Session = Depends(get_db)):
    scores = db.query(Score).filter(Score.team_id == team_id).all()
    if not scores:
        return CommonResponse(False, None, 400, "조회된 악보가 없습니다.")
    
    for score in scores:
        score.is_deleted = True

    db.commit()
    
    return CommonResponse(
        True,
        {
            "message":"악보 삭제 성공"   
        },
        200, "악보 삭제 성공!"
        )

@rScore.post('/{team_id}', tags = ['score'], response_model=BaseResponse)
def upload_score():
    co.createEmptyScore(f"{os.getcwd()}/scoreRecognition/Output/img/emptyScore.png")
    up.upload_file_to_s3(f"{os.getcwd()}/scoreRecognition/Output/img/emptyScore.png", "emptyScore.png")

    return CommonResponse(
        True,
        {
            "message":"빈 악보 생성"   
        },
        200, "빈 악보 생성 성공!"
        )