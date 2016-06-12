$(document).ready(function() {

    var socket;
    var messages;
    var audioToggle = true;

    $('#audio-toggle').on('change', function(event) {
        console.log($(this).prop('checked'));
        if ($(this).prop('checked')) {
            audioToggle = true;
        } else {
            audioToggle = false;
        }
    });

    var init = function() {
        $.ajax({
            url: '/api/messages',
            method: 'GET',
            success: function(data) {
                console.log(data);
                //messages = $.parseJSON(data);
                //console.log(messages);
                appendBroadcasts(data);
            }
        });
        socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
            socket.emit('initEvent', {data: 'I\'m connected!"'});
        });
        socket.on('initResponse', function(response) {
            console.log(response);
        });
        socket.on('messageResponse', function(response) {
            console.log(response);
            if (audioToggle) {
                $('#audio-' + response['messageID'])[0].play();
            }
            $('#broadcast').prepend(response['html']);
        });
        renewUser();
    };

    var appendBroadcasts = function(messages) {
        $.ajax({
            url: '/api/broadcasts',
            method: 'GET',
            success: function(data) {
                var broadcasts = $.parseJSON(data);
                $($.parseJSON(data)).each(function() {
                    if (messages[this['messageID']]) {
                        var date = new Date(parseInt(this['createdTime']) * 1000);
                        $('#broadcast').append(
                            '<div class="message-panel">' +
                                '<div class="message-username">' +
                                    '<span class="name">' +
                                        this['broadcasterData']['displayName'] +
                                    '</span>' +
                                    ' broadcasted:' +
                                '</div>' +
                                '<div class="message-broadcast">' +
                                    messages[this['messageID']]['text'] +
                                '</div>' +
                                '<div class="message-timestamp">' + date.toISOString() + '</div>' +
                            '</div>'
                        );
                        console.log(this);
                    }
                });
            }
        });
    };

    var renewUser = function() {
        window.setInterval(
            function() {
                $.ajax({
                    url: '/api/signon/renew',
                    method: 'POST',
                    success: function(data) {
                        console.log(data);
                    }
                });
            },
            15 * 60 * 1000
        );
    };

    var sessionID = $('#sessionID').val();
    if (sessionID) {
        init();
    } else {
        $('#signon-modal').modal({
            'backdrop': 'static'
        });
        $('#signon-modal').modal('show');
        $('#signon').submit(function(event) {
            $.ajax({
                url: '/api/signon',
                method: 'POST',
                data: {
                    displayName: $('#displayName').val()
                },
                success: function(data) {
                    $('#signon-modal').modal('hide');
                    sessionID = data['sessionID'];
                    $('#sessionID').val(sessionID)
                    init();
                }
            });
            event.preventDefault();
        });
    }

    $('.message').each(function() {
        var $this = $(this);
        $this.find('.play').click(function(event) {
            $audio = $this.find('audio');
            console.log($audio);
            $audio[0].play();
            $(this).blur();
        });
        $this.find('.broadcast').click(function(event) {
            var data = {
                data: {
                    sessionID: sessionID,
                    messageID: $this.attr('id')
                }
            }
            socket.emit('messageEvent', data);
            $(this).blur();
        });
    });

    $('.header').on('affixed.bs.affix', function(event) {
        $(this).animate({
            opacity: 0
        }, 500, function() {
            $(this).css('visibility', 'hidden');
        });
    });

    $('.header').on('affixed-top.bs.affix', function(event) {
        $(this).css('visibility', 'visible');
        $(this).animate({
            opacity: 0.5
        }, 500, function() {
        });
    });

    /*
    $('#client-input').submit(function(e) {
        console.log($(this).find('textarea').val());
        socket.emit('messageEvent', {
            data: {
                message: $(this).find('textarea').val()
            }
        });
        e.preventDefault();
    });
    */

});