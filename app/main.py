from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database.db_query import DBQuery
from app.scripts.scraper import Scraper
import time

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root():
  return RedirectResponse(url='/docs')

@app.get("/drugs")
def read_drugs():
  return DBQuery.get_all("drugs")

@app.put("/rewrite-db")
def rewrite_db():
  start = time.time()
  Scraper.scrap_all_drugs()
  end = time.time()
  
  elapsed_time_seconds = end - start
  elapsed_time_readable = "{:.1f}".format(elapsed_time_seconds)
  
  return {"DB reloaded in": f"{elapsed_time_readable}s"}