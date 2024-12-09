from app.dao.base import BaseDAO
from app.models.accidents import Accidents


class AccidentDAO(BaseDAO):

    model = Accidents
