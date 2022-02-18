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
        await self.login()#login to hq
        await self.get_info()#get customer info
        self.customer = self.customers[0]
        await self.customer.get_info()#get accounts info
        self.account = self.customer.accounts[0]
        self.contract = self.account.contracts[0]
        self.winter_credit = self.contract.winter_credit
        await self.contract.winter_credit.refresh_data()#get winter credit data
        self.wc_events = await self.contract.winter_credit.get_all_events()

    async def close_fut(self):
        await self.close_session()

    def get_events(self):
        loop= asyncio.get_event_loop()
        loop.run_until_complete(self.async_func())
        loop.run_until_complete(self.close_fut())

        return self.wc_events

if __name__ == "__main__":
    """
    part to be able to test outside of webthings gateway
    """
    hqWebUser = hq_webuser('USERNAME', 'PASSWORD')
    events = hqWebUser.get_events()
    print("TEST DATA: {0}".format(events))
