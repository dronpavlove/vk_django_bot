import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from django.conf import settings
from products.models import Category, Product

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()
vk_upload = VkUpload(vk)

keyboard = VkKeyboard(one_time=False, inline=True)
section_dict = {i.category_name: i.id for i in Category.objects.filter(activity=True)}
for elem, value in section_dict.items():
	keyboard.add_button(elem)


def send_message(**kwargs):
	"""
	Отдаёт сообщение пользователю в зависимости от задачи
	(в группу или лично пользователю,
	с клавиатурой или без неё,
	с фото или без фото)
	"""
	post = {
		'keyboard': keyboard.get_keyboard(),
		'random_id': 0,
		'peer_id': kwargs['event']['from_id'],
		'message': kwargs['message']
	}
	for element in kwargs['event']:
		if element == "group_id":
			post['chat_id'] = element["group_id"]
# 			elif kwargs['event'].from_chat:
# 				post['chat_id'] = kwargs['event'].chat_id
#  		elif element == 'keyboard':
# 			if kwargs['keyboard'] is False:
# 				post.pop('keyboard')
# 		else:
# 		post[element] = kwargs[element]
	vk.messages.send(**post)


def button_response(section_id: int):
	"""
	В зависимости от выбранной категории (по нажатию кнопки)
	возвращает соответствующую продукцию с описанием, с фотографией
	"""
	products = {}

	if len(products) == 0:
		yield {'message': 'В базе продукция сейчас не найдена. Попробуйте позже...', 'attachment': '543'}
	else:
		for product in products:
			text = str(product['name']) + '\n' + str(product['description'])
			attachment = product['attachment']
			yield {'message': text, 'attachment': attachment}
