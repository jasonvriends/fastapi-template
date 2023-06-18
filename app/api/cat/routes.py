from datetime import date, datetime, time
from typing import List, Optional
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId, init_beanie
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from api.cat.models import Cat
from config.fief_client import FiefAccessTokenInfo, FiefUserInfo, auth

router = APIRouter()


@router.get("/", response_model=List[Cat])
async def get_cats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Retrieves a list of the user's cats.

    **Args**:
    - **start_date** `Optional[datetime]` \n
      - Defaults to the current date in the user's timezone or UTC if none is provided.
    - **end_date** `Optional[datetime]` \n
      - Defaults to the current date in the user's timezone or UTC if none is provided.

    **Returns**:
    - `List[Cat]` \n
      - A list of cats that are within the start_date and end_date.
    """

    # Set the start_date if it's None
    if start_date is None:
        start_date = datetime.combine(date.today(), time.min)

    # Set the end_date if it's None
    if end_date is None:
        end_date = datetime.combine(date.today(), time.max)

    # Retrieve all cats from the database associated to the logged in user
    result = await Cat.find(
        Cat.user_id == user["sub"],
        Cat.created_on >= start_date,
        Cat.created_on <= end_date,
    ).to_list()

    return result


@router.post("/", response_model=Cat)
async def create_cats(
    cat: Cat,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Create a new cat associated to the user.

    **Args**:
    - **cat** `Cat` \n

    **Returns**:
    - `Cat` \n
    """

    # Set user_id to user
    cat.user_id = user["sub"]

    # Insert cat into the database
    await cat.insert()

    # Return the cat
    return cat


@router.get("/{cat_id}", response_model=Cat)
async def get_cat(
    cat_id: PydanticObjectId,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Retrieves a user's cat by ID.

    **Args**:
    - **cat_id** `PydanticObjectId` \n
      - The ID of the cat item to retrieve.

    **Raises**:
    - `HTTPException` \n
      - 404: cat not found
      - 403: Unauthorized access

    **Returns**:
    - `Cat` \n
    """

    # Retrive cat from the database
    cat = await Cat.get(cat_id)

    if not cat:
        # Cat not found
        raise HTTPException(status_code=404, detail="Cat not found")

    # Verify cat user_id and logged in user match
    if str(cat.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Return the cat
    return cat


@router.put("/{cat_id}", response_model=Cat)
async def update_cat(
    cat_id: PydanticObjectId,
    cat: Cat,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Updates a user's cat by ID.

    **Args**:
    - **cat_id** `PydanticObjectId` \n
      - The ID of the cat item to update.
    - **cat** `Cat` \n
      - The cat to be updated.

    **Raises**:
    - `HTTPException` \n
      - 404: Cat not found
      - 403: Unauthorized access

    **Returns**:
    - `Cat` \n
    """

    # Retrive cat from the database
    existing_cat = await Cat.get(cat_id)

    if not existing_cat:
        # cat not found
        raise HTTPException(status_code=404, detail="Cat not found")

    # Verify cat user_id and logged in user match
    if str(existing_cat.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Update only changed fields
    for field in cat.__fields__:
        field_value = getattr(cat, field)
        if field_value is not None:
            print({field: field_value})
            await existing_cat.set({field: field_value})

    return existing_cat


@router.delete("/{cat_id}")
async def delete_consumable(
    cat_id: PydanticObjectId,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Deletes a user's cat by ID.

    **Args**:
    - **cat_id** `PydanticObjectId` \n
      - The ID of the cat item to delete.

    **Raises**:
    - `HTTPException` \n
      - 404: Cat not found
      - 403: Unauthorized access

    **Returns**:
    - `str` \n
    """

    # Retrive cat from the database
    cat = await Cat.get(cat_id)

    if not cat:
        # Cat not found
        raise HTTPException(status_code=404, detail="Cat not found")

    # Verify cat user_id and logged in user match
    if str(cat.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    await cat.delete()

    return {"message": "Cat deleted"}
