"""Web user class for HQ website connection to pull """

import asyncio
import sys
import os

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from hydroqc import webuser

class hq_webuser(webuser.WebUser):
    """HQ web user connection"""
    
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
        """
        get all peak events
        
        return events as list of dict {'start' : X, 'end' : Y }
        """
        events = []
        loop= asyncio.get_event_loop()
        loop.run_until_complete(self.async_func())
        loop.run_until_complete(self.close_fut())
        for event in self.wc_events:
            events.append({'start': event.to_dict()['start'], 'end': event.to_dict()['end']})


        return events

if __name__ == "__main__":
    """
    part to be able to test outside of webthings gateway
    """
    hqWebUser = hq_webuser('USERNAME', 'PASSWORD')
    events = hqWebUser.get_events()
    print(events)
