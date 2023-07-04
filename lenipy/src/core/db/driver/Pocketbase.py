from pocketbase import PocketBase
from lenipy.src.core.db.BaseDriver import BaseDriver
from lenipy.src.core.models.modules import Modules


class PocketbaseDriver(BaseDriver):

    def __init__(self, user, password, url):
        self.client: PocketBase = PocketBase(url)
        self.admin = self.client.admins.auth_with_password(user,password)

    def create_modules(self, modules: Modules):
        self.client.collection("modules").create(
                {
                    "url": modules.url,
                    "name": modules.name
                }
                )

    

    def get_modules_by_id(self, mod_id: str) -> Modules:
        module_raw = self.client.collection("modules").get_one(mod_id)
        
        data_mod_id = module_raw.id
        data_name = module_raw.name
        data_url = module_raw.url

        return Modules(mod_id=data_mod_id,
                       name=data_name,
                       url=data_url)

