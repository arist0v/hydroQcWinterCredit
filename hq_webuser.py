"""Web user class for HQ website connection to pull """

import asyncio

from hydroqc import webuser


class hq_webuser(webuser.WebUser):
    """HQ web user connection"""

    def __init__(self, username, password, verify_ssl=False, log_level=None, http_log_level=None):
        """
        init the object
        """
        #TODO:remove if not used
        super().__init__(username, password, verify_ssl, log_level, http_log_level)

    async def async_func(self):
        """async func"""
        await self.login()
        await self.get_info()


    


if __name__ == "__main__":
    hqWebUser = hq_webuser('verret.martin@gmail.com', 'b64214909B')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hqWebUser.async_func())
    close_fut = asyncio.wait([hqWebUser.close_session()])
    loop.run_until_complete(close_fut)
    #loop.close()

    print("TEST DATA: {0}".format(hqWebUser.customers[0]))
