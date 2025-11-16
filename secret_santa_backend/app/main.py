from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from .utils import read_employees_from_csv, read_previous_assignments_from_csv, write_assignments_to_csv
from .assigner import SecretSantaAssigner, Employee as Emp
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Secret Santa Assignment API")

@app.post("/assign")
async def assign_secret_santa(
    employees_csv: UploadFile = File(...),
    previous_csv: UploadFile | None = File(None)
):
    # Read employee CSV
    try:
        employees_stream = io.TextIOWrapper(employees_csv.file, encoding='utf-8')
        employees = read_employees_from_csv(employees_stream)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading employee CSV: {e}")
    # Read previous assignments
    previous_map = {}
    if previous_csv is not None:
        try:
            prev_stream = io.TextIOWrapper(previous_csv.file, encoding='utf-8')
            previous_map = read_previous_assignments_from_csv(prev_stream)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading previous CSV: {e}")

    # build assigner
    try:
        assigner = SecretSantaAssigner([Emp(name=e.name, email=e.email) for e in employees], previous_map)
        assignments = assigner.assign()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=422, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    # write output CSV to bytes
    output_buffer = io.StringIO()
    write_assignments_to_csv(assignments, output_buffer)
    output_buffer.seek(0)
    return StreamingResponse(iter([output_buffer.read().encode('utf-8')]),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=secret_santa_assignments.csv"})



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)