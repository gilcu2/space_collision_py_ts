from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import Optional
import uvicorn
import os
from datetime import datetime, date, timedelta
from discoweb_client import DiscosWebClient

from postgres import Postgres
from dotenv import load_dotenv

load_dotenv()

disco_web_token = os.environ["DISCOWEB_TOKEN"]
disco_web_client = DiscosWebClient(disco_web_token)
pg_url = os.getenv("PG_URL", "postgresql://localhost:5432/postgres?user=postgres&password=postgres")
postgres = Postgres(pg_url)


def download_data(begin, end, limit, suffix):
    launches_data = disco_web_client.get_launches(begin, end, page_size=limit).data
    launches_processed = [(launch['id'], launch['attributes']) for launch in launches_data]
    postgres.insert_data(f'launches{suffix}', launches_processed)

    reentries_data = disco_web_client.get_reentries(begin, end, page_size=limit).data
    reentries_processed = [(reentry['id'], reentry['attributes']) for reentry in reentries_data]
    postgres.insert_data(f'reentries{suffix}', reentries_processed)

    return launches_data, reentries_data


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/download_data/")
def download_data_endpoint(begin: date = datetime.strptime('2025-03-01', "%Y-%m-%d").date(),
                           end: date = datetime.strptime('2025-03-31', "%Y-%m-%d").date(),
                           limit: int = 30,
                           suffix: Optional[str] = None) -> dict:
    launches_data, reentries_data = download_data(begin, end, limit, suffix)

    return {'launches': len(launches_data), 'reentries': len(reentries_data)}


@app.get("/get_space_objects_variation/")
def get_space_objects_variation(begin: date = datetime.strptime('2025-01-01', "%Y-%m-%d").date(),
                                end: date = datetime.strptime('2025-01-31', "%Y-%m-%d").date(),
                                suffix: str = "",
                                ) -> dict:
    launches_per_day = postgres.get_number_by_day(f'launches{suffix}')
    reentries_per_day = postgres.get_number_by_day(f'reentries{suffix}')

    launches_dict = dict(launches_per_day)
    reentries_dict = dict(reentries_per_day)

    days = []
    variations = []
    for i in range((end - begin).days + 1):
        day = begin + timedelta(days=i)
        days.append(day)
        variations.append(launches_dict.get(day, 0) - reentries_dict.get(day, 0))

    return {'days': days, 'variations': variations}


if __name__ == "__main__":
    uvicorn.run("kpi_api:app", host='0.0.0.1', port=8000, reload=True)
else:
    rows = postgres.count_rows('launches')
    if rows == 0:
        print(f"App is starting up, downloading data...{rows}")
        download_data(
            datetime.strptime('2025-03-01', "%Y-%m-%d").date(),
            datetime.strptime('2025-03-10', "%Y-%m-%d").date(),
            100, ''
        )
        download_data(
            datetime.strptime('2025-04-11', "%Y-%m-%d").date(),
            datetime.strptime('2025-04-20', "%Y-%m-%d").date(),
            100, ''
        )
        download_data(
            datetime.strptime('2025-04-21', "%Y-%m-%d").date(),
            datetime.strptime('2025-04-31', "%Y-%m-%d").date(),
            100, ''
        )
        print("Data downloaded 2025-03-01 to 2025-03-31")
