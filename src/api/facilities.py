from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from exceptions import ObjectNotFoundException
from src.schemas.facilities import FacilityAddSchema
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"],
)


@router.get("")
@cache(expire=60)
async def get_all_facilities(db: DBDep):
    # facilities_from_cache = await redis_manager.get("facilities")
    # if not facilities_from_cache:
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set(
    #         key="facilities",
    #         value=facilities_json,
    #         expire=60
    #     )
    # else:
    #
    #     facilities = json.loads(facilities_from_cache)
    # return facilities

    return await db.facilities.get_all()


@router.get("/{facility_id}")
@cache(expire=60)
async def get_facility(db: DBDep, facility_id: int):
    print("Going to DB")
    try:
        query = await db.facilities.get_one(id=facility_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    return query


@router.post("")
async def add_facility(
    db: DBDep,
    facility: FacilityAddSchema = Body(
        openapi_examples={
            "1": {"summary": "Удобство: интернет", "value": {"name": "Интернет"}},
            "2": {"summary": "Удобство: кондиционер", "value": {"name": "Кондиционер"}},
        }
    ),
):
    query = await db.facilities.add(facility)
    await db.commit()
    return {"success": True, "data": query}
