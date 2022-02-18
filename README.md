# hydroQcWinterCredit
Webthings module to create an things for the winter credit from hydro quebec

Project:
create a webthings.io addons that will provide a things that provide the following informations:
-Active bool : a boolean that will be true if there is an active event Read only
-Next event : date of the next event Read only
-Last sync : last succeful sync of event Read only

The configuration needed so far:
-username: hydroquebec profil username
-password: hydroquebec profil password
-pre heat delay: delay in minutes before event to pre-heat
-post heat delay: delay in minutes after event to re heat

Goal:
the use of this thing will be to use this things to set rules to reduce the heating target of thermostat during the event period.
During those period you can get credit for each kwh not used(or in some case, the price of each kwh during those period are higher)

DONE:
-manifest.json with the configuration from end user

TODO:
-try to set the password field as password and not text

CREDIT:
Thank you to all those who have contributed to Hydro Quebec API Wrapper project : https://gitlab.com/hydroqc/hydroqc on wich i based part of my work

NOTE:
This project is not an official Hydro Quebec project.

