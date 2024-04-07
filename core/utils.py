
from fastapi import Query, HTTPException
from datetime import date, datetime

def date_validator(date_str: str = Query(date)):
    if date_str:
        try:
            valid_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Please send the date parameter as 'YYYY-MM-DD' format")
    return None
