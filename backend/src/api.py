from fastapi import FastAPI
from typing_extensions import Optional
import uvicorn
import os
from datetime import datetime, date, timedelta
from discoweb_client import DiscosWebClient

from postgres import Postgres
from dotenv import dotenv_values

config = dotenv_values(".env")

discoweb_client = DiscosWebClient(config["DISCOWEB_TOKEN"])
pg_url = os.getenv("PG_URL", "postgresql://localhost:5432/postgres?user=postgres&password=postgres")
postgres = Postgres(pg_url)

app = FastAPI()


@app.get("/download_data/")
def download_data(begin: date = datetime.strptime('2025-01-01', "%Y-%m-%d").date(),
                  end: date = datetime.strptime('2025-01-31', "%Y-%m-%d").date(),
                  limit: Optional[int] = None,
                  suffix: Optional[str] = None) -> dict:
    launches_data = discoweb_client.get_launches(begin, end).data
    launches_processed = [(launch['id'], launch['attributes']) for launch in launches_data]
    postgres.insert_data(f'launches{suffix}', launches_processed)
    reentries_data = discoweb_client.get_reentries(begin, end, page_size=limit).data
    reentries_processed = [(reentry['id'], reentry['attributes']) for reentry in reentries_data]
    postgres.insert_data(f'reentries{suffix}', reentries_processed)

    return {'launches': len(launches_data), 'reentries': len(reentries_data)}


@app.get("/get_space_objects_variation/")
def get_space_objects_variation(begin: date = datetime.strptime('2025-01-01', "%Y-%m-%d").date(),
                                end: date = datetime.strptime('2025-01-31', "%Y-%m-%d").date(),
                                suffix: Optional[str] = None,
                                ) -> list[tuple]:
    launches_per_day=postgres.get_number_by_day(f'launches{suffix}')
    reentries_per_day=postgres.get_number_by_day(f'reentries{suffix}')

    launches_dict=dict(launches_per_day)
    reentries_dict=dict(reentries_per_day)

    variations=[]
    for i in range((end - begin).days + 1):
        day = begin + timedelta(days=i)
        variations.append((day,launches_dict.get(day,0) - reentries_dict.get(day,0)))


    return variations


if __name__ == "__main__":
    uvicorn.run("kpi_api:app", host='0.0.0.1', port=8000, reload=True)
