import json
import cgi
import time
import datetime
import eventlet
import socketio
import lib.bottle.bottle as bottle
from api.broadcasts_response import BroadcastsResponse

sio = socketio.Server()

@sio.on('connect')
def connect(sid, env):
    #print('connect ', sid)
    True

@sio.on('disconnect')
def disconnect(sid):
    #print('disconnect ', sid)
    True

@sio.on('initEvent')
def handle_event(sid, json):
    sio.emit('initResponse', {'serverTime' : int(time.time())})

@sio.on('messageEvent')
def handle_event(sid, json):
    #time.sleep(20)
    #return {}
    messageID = json['data']['messageID']
    sessionID = json['data']['sessionID']
    from api.signon_response import SignonResponse
    signonResponse = SignonResponse()
    user = signonResponse.get_user_from_session_id(sessionID)
    if not user:
        return {}
    #cgi.escape(json['data']['message'])
    broadcastsResponse = BroadcastsResponse()
    message, broadcastID = broadcastsResponse.process_broadcast(messageID, user)
    if message:
        timestamp = time.time()
        dt = datetime.datetime.utcnow()
        formattedTime = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        timestamp = dt.timestamp()
        displayName = user.displayName
        sio.emit('messageResponse', {
            'messageID' : message.id,
            'messageURL' : message.url,
            'broadcastID' : broadcastID,
            'html' : bottle.template(
                'elements-message-panel',
                message=message,
                displayName=displayName,
                formattedTime=formattedTime
            )
        })

deployTag = open('deploy_tag', 'r').read().strip()
app = bottle.Bottle()

@app.route('/')
@app.route('/app')
def render_index():
    from api.broadcasts_response import BroadcastsResponse
    broadcastsResponse = BroadcastsResponse()
    messages = broadcastsResponse.get_all_messages()
    messageInputs = bottle.template('elements-message-input', messages=messages)
    #print(messageInputs)
    from api.signon_response import SignonResponse
    signonResponse = SignonResponse()
    user = signonResponse.get_user_from_session()
    if user:
        sessionID = user.id
    else:
        sessionID = ''
    return bottle.template(
        'index',
        deployTag=deployTag,
        messageInputs=messageInputs,
        sessionID=sessionID
    )

# TODO: In the future, support inputting n, size of output.
@app.get('/api/broadcasts')
@app.get('/api/broadcasts/')
def get_broadcasts():
    from api.broadcasts_response import BroadcastsResponse
    broadcastsResponse = BroadcastsResponse()
    response = broadcastsResponse.get_last_broadcasts_response(10)
    return json.dumps(response)

@app.get('/api/messages')
@app.get('/api/messages/')
def get_broadcasts():
    from api.broadcasts_response import BroadcastsResponse
    broadcastsResponse = BroadcastsResponse()
    messages = broadcastsResponse.get_all_messages_response()
    return messages

@app.post('/api/signon')
@app.post('/api/signon/')
def handle_signon():
    from api.signon_response import SignonResponse
    signonResponse = SignonResponse()
    sessionID = signonResponse.signon(
        bottle.request.POST.get('displayName')
    )
    return {'sessionID' : sessionID}

@app.post('/api/signon/renew')
@app.post('/api/signon/renew/')
def handle_signon():
    from api.signon_response import SignonResponse
    signonResponse = SignonResponse()
    user = signonResponse.get_user_from_session()
    if user:
        sessionID = user.id
    else:
        sessionID = ''
    return {'sessionID' : sessionID}

@app.route('/api/signout')
@app.route('/api/signout/')
def handle_signout():
    '''Kill User's session.
    '''
    from api.signon_response import SignonResponse
    signonResponse = SignonResponse()
    sessionID = signonResponse.signon(
        bottle.request.POST.get('displayName')
    )
    signonResponse.signout(bottle.request.get_cookie('sessionID'))
    return {'response' : 'Signed out.'}

@app.route('/static/<path:path>')
def static_respond(path):
    return bottle.static_file(path, root='static')

'''
#app = flask.Flask(__name__)
#app.config['SECRET_KEY'] = open('secret', 'r').read()
@app.route('/')
def render_index():
    return flask.render_template('index.html')
@app.route('/signon', methods=['PUT'])
def handle_signon():
    # TODO: If user is already logged in, return success.
    displayName = flask.request.form['displayName']
    return {'status' : 'success'}
@app.route('/api/message', methods=['PUT'])
def handle_message():
    print(flask.request.form['message'])
    return 'Success'
@app.route('/static/<path:path>')
def static_respond(path):
    return flask.send_from_directory('static', path)
'''

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)