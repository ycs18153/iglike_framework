from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import Model, updateModel

router = APIRouter()


@router.post("/", response_description="Add new user")
async def create_user(request: Request, user: Model = Body(...)):
    user = jsonable_encoder(user)
    new_user = await request.app.mongodb["auth_user"].insert_one(user)
    created_user = await request.app.mongodb["auth_user"].find_one(
        {"_id": new_user.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["auth_user"].find().to_list(length=100):
        users.append(doc)
    return users


@router.get("/{id}", response_description="Get a user")
async def show_user(id: str, request: Request):
    if (user := await request.app.mongodb["auth_user"].find_one({"uid": id})) is not None:
        return user
    else:
        return '-1'
        

    raise HTTPException(status_code=404, detail=f"user {id} not found")


# @router.put("/{id}", response_description="Update a task")
# async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
#     task = {k: v for k, v in task.dict().items() if v is not None}

#     if len(task) >= 1:
#         update_result = await request.app.mongodb["tasks"].update_one(
#             {"_id": id}, {"$set": task}
#         )

#         if update_result.modified_count == 1:
#             if (
#                 updated_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#             ) is not None:
#                 return updated_task

#     if (
#         existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#     ) is not None:
#         return existing_task

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")


# @router.delete("/{id}", response_description="Delete Task")
# async def delete_task(id: str, request: Request):
#     delete_result = await request.app.mongodb["tasks"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")
