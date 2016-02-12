% for message in messages:
<div class="form-group">
    <div id="{{message.id}}" class="btn-group message" role="group">
        <button type="button" class="btn btn-default broadcast">
            Broadcast
            <span class="glyphicon glyphicon-bullhorn"></span>
        </button>
        <button type="button" class="btn btn-default play">
            <span class="glyphicon glyphicon-play"></span>
        </button>
        <audio id="audio-{{message.id}}" visibility="hidden" src="{{message.url}}" preload="auto"></audio>
    </div>
    {{message.text}}
</div>
% end