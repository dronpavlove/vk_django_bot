import time
import vk_api
from vk_api import VkUpload
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
from products.views import get_products_dict, get_category_dict

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()
vk_upload = VkUpload(vk)

timer = 0


def send_message(**kwargs):
	"""
	Отдаёт сообщение пользователю в зависимости от задачи
	(в группу или лично пользователю,
	с клавиатурой или без неё,
	с фото или без фото)
	"""

	post = {
		'keyboard': kwargs['event']['keyboard'],
		'random_id': 0,
		'peer_id': kwargs['event']['from_id'],
		'message': kwargs['message']
	}
	for element in kwargs:
		if element == 'attachment':
			post['attachment'] = kwargs['attachment']
		elif element == 'keyboard':
			post.pop('keyboard')

	vk.messages.send(**post)


def button_response(section_id: int):
	"""
	В зависимости от выбранной категории (по нажатию кнопки)
	возвращает соответствующую продукцию с описанием, с фотографией
	"""
	products = get_product_objects(section_id)

	if len(products) == 0:
		yield {'message': 'В базе продукция сейчас не найдена. Попробуйте позже...', 'attachment': '543'}
	else:
		for product in products:
			text = str(product['name']) + '\n' + str(product['description'])
			attachment = product['attachment']
			yield {'message': text, 'attachment': attachment}


def get_product_objects(section: int):
	"""
	Возвращает список продукции в зависимости от выбранной категории.
	"""
	full_products = cache.get_or_set('full_products', {})
	if edit_timer() is True or section not in full_products:
		update_data()
	products = full_products[section]
	return products


def get_section_dict():
	"""
	Возвращает список разделов.
	"""
	sections = cache.get_or_set('sections', {})
	if edit_timer() is True or len(sections) == 0:
		update_data()
	return sections


def edit_timer(period=24):
	"""
	Определяет периодичность обновления глобальных переменных
	full_products = dict()
	sections = dict()
	По умолчанию 24 часа
	"""
	global timer
	current_time = int(time.strftime('%H', time.localtime()))
	if current_time > timer:
		difference = current_time - timer
	else:
		difference = 24 - timer + current_time
	if difference >= period:
		timer = current_time
		return True
	else:
		return False


def send_photo(url):
	"""
	Расширяет объект Product полем 'attachment'
	(прогружает фото в ВК и сохраняет данные для
	ускорения отправки ответных сообщений)
	"""
	upload = vk_api.VkUpload(vk)
	try:
		photo = upload.photo_messages(url)
	except FileNotFoundError:
		photo = upload.photo_messages('media/default.png')
	owner_id = photo[0]['owner_id']
	photo_id = photo[0]['id']
	access_key = photo[0]['access_key']
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	return attachment


def update_data(request=None):
	"""
	Возвращает список продукции в зависимости от выбранной категории.
	Обращается или к БД (длительный процесс),
	или к глобальной переменной (для ускорения процесса)
	"""
	full_products = cache.get_or_set('full_products', {})
	sections = cache.get_or_set('section', get_category_dict())
	for section_id in sections.values():
		product_list = get_products_dict(section_id)
		if section_id not in full_products:
			products = [{
				'name': i['name'], 'description': i['description'], 'photo': i['photos'][0],
				'attachment': send_photo(i['photos'][0])
			} for i in product_list]
			full_products[section_id] = products
		else:
			photo_list = [i['photo'] for i in full_products[section_id]]
			for product in product_list:
				if product['photos'][0] not in photo_list:
					products = {
						'name': product['name'],
						'description': product['description'],
						'photo': product['photos'][0],
						'attachment': send_photo(product['photos'][0])
					}
					full_products[section_id].append(products)
	cache.set('full_products', full_products)
	cache.set('sections', sections)
	return HttpResponse('Кэш обновился', status=200)
