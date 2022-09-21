from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json
from vk_api.keyboard import VkKeyboard

from bot_logic.vk_bot_logic import send_message, button_response
from products.views import get_category_dict


@csrf_exempt
def index(request):
	if request.method == "POST":
		section_dict = get_category_dict()
		data = json.loads(request.body.decode('utf-8'))
		message_data = data['object']['message']
		keyboard = VkKeyboard(one_time=False, inline=True)
		for elem, value in section_dict.items():
			keyboard.add_button(elem)
		message_data['keyboard'] = keyboard.get_keyboard()
		clean_text = message_data['text']
		if data['type'] == 'confirmation':  # if VK server request confirmation
			return settings.VK_GET_KEY

		elif data['type'] == 'message_new':

			if clean_text in section_dict:
				category_id = section_dict[clean_text]
				send_message(
					message=f'Запрос принят. Минуточку... Сейчас обрабатывается запрос {clean_text}: id={category_id}',
					event=message_data, keyboard=False
				)
				for i in button_response(category_id):
					send_message(message=i['message'], event=message_data, attachment=i['attachment'], keyboard='None')

				send_message(message='Продолжим...', event=message_data)

				return HttpResponse('ok', content_type="text/plain", status=200)
			else:
				send_message(event=message_data, message=f'Ответ на простое сообщение, не на кнопку... \n {clean_text}')
				return HttpResponse('ok', content_type="text/plain", status=200)
	else:
		return HttpResponse('see you :)')
