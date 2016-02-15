# Frustratio

## Environment Setup

### Requirements
- Linux-based environment (not tested on OS X or Windows), preferably Ubuntu.
- Python 3.

### Set Up Python Virtual Environment Per Project
```
virtualenv /path/to/project/venv/
```
### Activate Virtual Environment
```
source /path/to/project/venv/bin/activate
```
### Deactivate Virtual Environment
```
deactivate
```

### Install Python-SocketIO
```
source /path/to/project/venv/bin/activate
pip3 install python-socketio
deactivate
```

### Install Eventlet
```
source /path/to/project/venv/bin/activate
pip3 install eventlet
deactivate
```

### Install Nose And Coverage For Unit Testing
```
source /path/to/project/venv/bin/activate
pip3 install nose
pip3 install coverage
deactivate
```
### To Run:
```
nosetests
```
### For More Detailed Reporting:
```
sh coverage.sh
```

### Configure MongoDB Data Store (Temporary Until Postgres 9.4 Package Available)
- Install MongoDB To System (Assuming Debian Environment)
```
sudo aptitude install mongodb
```
- Install PyMongo MongoDB Driver
```
source /path/to/project/venv/bin/activate
pip3 install pymongo
deactivate
```

### Configure Redis Data Store (For Sessions)
- Install Redis To System (Assuming Debian Environment)
```
sudo aptitude install redis-server
```
- Install Redis Driver
```
source /path/to/project/venv/bin/activate
pip3 install redis
deactivate
```

### Install Passlib For Password Hashing
```
source /path/to/project/venv/bin/activate
pip3 install passlib
deactivate
```

### Create Required Non-Version-Controlled Files
.gitignore
deploy_tag