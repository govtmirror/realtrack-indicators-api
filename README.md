Realtrack Indicators Demo API
---
This is a small Flask web app that I hacked up to demo the use of an API for Realtrack Indicators. It runs off the same SQLite database that is used by the Realtrack Android app.

A live version of this app can be viewed at [http://neeraj2608.pythonanywhere.com](http://neeraj2608.pythonanywhere.com/) (I chose [pythonanywhere](www.pythonanywhere .com) because they are one of the few providers that allow deploying Flask apps with SQLite).

A sample API call is shown below:

<code>
http://neeraj2608.pythonanywhere.com/indicators?project=Education&country=Thailand
</code>

This returns indicators for 'Thailand' and 'Education' in JSON format.
