from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json

from bot_logic.vk_bot_logic import send_message, section_dict, button_response, vk_session, vk, vk_upload


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))  # take POST request from auto-generated variable <request.body> in json format
        if data['type'] == 'confirmation':# if VK server request confirmation
            return settings.VK_GET_KEY
        elif data['type'] == 'message_new':# if VK server send a message
            from_id = data['object']['message']['from_id']
            vk.messages.send(
                message=f'Hello World! {str(data)}',
                random_id=0,
                peer_id=from_id
            )
            send_message(event=data['object']['message'], message='Ну вот ещё')
            return HttpResponse('ok', content_type="text/plain", status=200)
    else:
        return HttpResponse('see you :)')
