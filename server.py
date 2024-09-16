import json

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Base, Session, User, engine, Advertisement


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


app = web.Application()


async def orm_context(app: web.Application):
    print("Start")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("Shut down")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_cls, error_description):
    return error_cls(
        text=json.dumps({"error": error_description}), content_type="application/json"
    )


# async def get_user(user_id: int, session: Session):
#     user = await session.get(User, user_id)
#     if user is None:
#         raise get_error(web.HTTPNotFound, "user not found")
#     return user
#
#
# async def add_user(user: User, session: Session):
#     session.add(user)
#     try:
#         await session.commit()
#     except IntegrityError:
#         error = get_error(web.HTTPConflict, "user already exists")
#         raise error
#     return user


async def get_adv(adv_id: int, session: Session):
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise get_error(web.HTTPNotFound, "adv not found")
    return adv


async def add_adv(adv: Advertisement, session: Session):
    session.add(adv)
    try:
        await session.commit()
    except IntegrityError:
        error = get_error(web.HTTPConflict, "adv already exists")
        raise error
    return adv


# class UserView(web.View):
#
#     @property
#     def session(self):
#         return self.request.session
#
#     @property
#     def user_id(self):
#         return int(self.request.match_info["user_id"])
#
#     async def get(self):
#         user = await get_user(self.user_id, self.session)
#         return web.json_response(user.json)
#
#     async def post(self):
#         json_data = await self.request.json()
#         json_data["password"] = hash_password(json_data["password"])
#         user = User(**json_data)
#         user = await add_user(user, self.session)
#         return web.json_response({"id": user.id})
#
#     async def patch(self):
#         json_data = await self.request.json()
#         if "password" in json_data:
#             json_data["password"] = hash_password(json_data["password"])
#         user = await get_user(self.user_id, self.session)
#         for field, value in json_data.items():
#             setattr(user, field, value)
#         user = await add_user(user, self.session)
#         return web.json_response({"id": user.id})
#
#     async def delete(self):
#         user = await get_user(self.user_id, self.session)
#         await self.session.delete(user)
#         await self.session.commit()
#         return web.json_response({"status": "deleted"})


class AdvertisementView(web.View):

    @property
    def session(self):
        return self.request.session

    @property
    def advertisement_id(self):
        return int(self.request.match_info["advertisement_id"])

    async def get(self):
        adv = await get_adv(self.advertisement_id, self.session)
        return web.json_response({'id': adv.id,
            'heading': adv.heading,
            'description': adv.description,
            'user_id': adv.user_id})

    async def post(self):
        advertisement_data = await self.request.json()
        new_advertisement = Advertisement(**advertisement_data)
        new_advertisement = await add_adv(new_advertisement, self.session)
        print(new_advertisement)
        return web.json_response({
            'id': new_advertisement.id,
            'heading': new_advertisement.heading,
            'description': new_advertisement.description,
            'user_id': new_advertisement.user_id,
        })

    async def patch(self):
        json_data = await self.request.json()

        adv = await get_adv(self.advertisement_id, self.session)
        for field, value in json_data.items():
            setattr(adv, field, value)
        adv = await add_adv(adv, self.session)
        #return web.json_response({"id": user.id})


        return web.json_response({
            'id': adv.id,
            'heading': adv.heading,
            'description': adv.description,
            'user_id': adv.user_id
        })

    async def delete(self):
        # adv = await get_adv(self.advertisement_id, self.session)
        # # adv = await get_adv(self.adv_id, self.session)
        # await self.session.delete(adv)
        # await self.session.commit()
        # return web.json_response({"status": "deleted"})

        adv = await get_adv(self.advertisement_id, self.session)
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


# app.add_routes(
#     [
#         web.post("/user/", UserView),
#         web.get("/user/{user_id:\d+}/", UserView),
#         web.patch("/user/{user_id:\d+}/", UserView),
#         web.delete("/user/{user_id:\d+}/", UserView),
#     ]
# )

app.add_routes(
    [
        web.post('/adv/', AdvertisementView),
        web.get("/adv/{advertisement_id:\d+}/", AdvertisementView),
        web.patch('/adv/{advertisement_id:\d+}/', AdvertisementView),
        web.delete('/adv/{advertisement_id:\d+}/', AdvertisementView),
    ]
)

web.run_app(app)
