from fastapi import APIRouter, Body, HTTPException

from schemas.facilities import FacilitySchema, FacilityAddSchema
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"],
)


@router.get("/")
async def get_all_facilities(
        db: DBDep
):
    return await db.facilities.get_all()


@router.get("/{facility_id}")
async def get_facility(
        db: DBDep,
        facility_id: int
):
    query = await db.facilities.get_one_or_none(id=facility_id)
    if query is None:
        raise HTTPException(status_code=404, detail=f"Facility with id {facility_id} not found.")
    return query


@router.post("/")
async def add_facility(
        db: DBDep,
        facility: FacilityAddSchema = Body(openapi_examples={
            "1": {"summary": "Удобство: интернет", "value":{"name": "Интернет"}},
            "2": {"summary": "Удобство: кондиционер", "value":{"name": "Кондиционер"}}
        })
):
    query = await db.facilities.add(facility)
    await db.commit()
    return {"success": True, "data": query}
