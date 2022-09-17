from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json

from bot_logic.vk_bot_logic import send_message, section_dict, button_response


@csrf_exempt
def index(request):
	body = json.loads(request.body)
	if body == settings.VK_BODY_DATA:
		return HttpResponse(settings.VK_GET_KEY)
	elif body['type'] == 'message_new':
		msg = body['object']['message']['text']
		user_id = body['object']['message']['from_id']
		send_message(event=body, message=f'Какой-то текст {msg}, {user_id}')
