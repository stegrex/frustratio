# 2016-02-12

- Fully implemented signon and signout functionality.
- Built persistent storage for broadcasts. Stored into MongoDB.
    - Added new method for replacing documents in MongoDB driver.
    - Added caching of broadcasts using Redis.
    - Built endpoint for query last n number of broadcasts.
    - Used linked list pattern to more easily handle loading last n number of
        items without benefit of querying by timestamps in the datastore.
- Cleaned up frontend functionality and layout.
    - Added custom CSS styles.
    - Implemented loading of last n number of broadcasts upon signon.
- Fixed various bugs.

# 2016-02-11

- Migrated over to python-socketio from flask-socketio to avoid being tied down
    specifically to Flask.
- Migrated over from Flask to Bottle.
- Added simple signon system for users, with no persistent user storage.
- Added some Bootstrap to support the frontend.

# 2016-02-10

- Built basic functionality for WebSocket app.
- Installed eventlet as recommended to run flask-socketio.
- Found separate library python-socketio for future research.
- Installed Nginx to forward requests to 127.0.0.1:5000 which is the default IP
    for running the Socket.IO app with eventlet.
- Tested on local network and found that Nginx was properly enabling clients on
    the network to access the app.