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

Goal:
the use of this thing will be to use this things to set rules to reduce the heating target of thermostat during the event period.
During those period you can get credit for each kwh not used(or in some case, the price of each kwh during those period are higher)

