<!DOCTYPE html>

<html>

<head>
    <title>frustrat.io</title>
    <script src="/static/lib/socket.io-1.4.5.js?{{deployTag}}"></script>
    <script src="/static/lib/jquery-2.2.0.js?{{deployTag}}"></script>
    <script src="/static/lib/bootstrap-3.3.6-dist/js/bootstrap.min.js?{{deployTag}}"></script>
    <script src="/static/js/frustratio.js?{{deployTag}}"></script>
    <link rel="stylesheet" href="/static/lib/bootstrap-3.3.6-dist/css/bootstrap.min.css?{{deployTag}}" />
    <link rel="stylesheet" href="/static/css/frustratio.css?{{deployTag}}" />

    <link href="https://gitcdn.github.io/bootstrap-toggle/2.2.0/css/bootstrap-toggle.min.css" rel="stylesheet">
    <script src="https://gitcdn.github.io/bootstrap-toggle/2.2.0/js/bootstrap-toggle.min.js"></script>

    <meta charset="utf-8">
    <meta name="description" content="frustrat.io: Broadcast your frustration.">
    <meta name="keywords" content="frustrat.io">
    <meta name="author" content="maxchen675">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <div class="header" data-spy="affix" data-offset-top="150">
        <h1>frustratio</h1>
        <h2>Broadcast your frustration.</h2>
        <a class="btn btn-default pull-right" href="/api/signout">Sign out</a>
    </div>
    <div class="container">
        <input type="hidden" id="sessionID" name="sessionID" value="{{sessionID}}" />
        <form id="client-input" class="main">
            <div class="alert alert-info" role="alert">
                New features and messages are currently being developed! Stay tuned for new stuff!
            </div>
            <div class="form-group">
                <input id="audio-toggle" checked data-toggle="toggle" type="checkbox" />
                <span class="glyphicon glyphicon-volume-up"></span>
            </div>
            {{!messageInputs}}
            <!--
            <div class="form-group">
                <textarea></textarea>
            </div>
            <div>
                <button type="submit" class="btn btn-default">Submit</button>
            </div>
            -->
        </form>
        <div id="broadcast" class="well"></div>
    </div>
    <div class="modal fade" id="signon-modal" tabindex="-1" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <form id="signon">
                    <div class="modal-header">
                        <!--
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        -->
                        <h4 class="modal-title">Create a temporary username</h4>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="displayName">Username</label>
                            <input type="text" class="form-control" id="displayName" name="displayName" />
                        </div>
                    </div>
                    <div class="modal-footer">
                        <!--<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>-->
                        <button type="submit" class="btn btn-default">Sign on</button>
                    </div>
                </form>
            </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
    </div><!-- /.modal -->
</body>

</head>