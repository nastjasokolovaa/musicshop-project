from datetime import datetime
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"http://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max_orig&v=5.92&access_token={response['access_token']}"

    vk_response = requests.get(api_url)

    if vk_response.status_code != 200:
        return

    vk_data = vk_response.json()['response'][0]

    if vk_data['sex']:
        if vk_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif vk_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if vk_data['about']:
        user.shopuserprofile.about_me = vk_data['about']

    if vk_data['bdate']:
        bdate = datetime.strptime(vk_data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if vk_data['photo_max_orig']:
        photo_link = vk_data['photo_max_orig']
        photo_response = requests.get(photo_link)
        user_photo_path = f'user_avatars/{user.pk}.jpg'
        with open(f'media/{user_photo_path}', 'wb') as photo_file:
            photo_file.write(photo_response.content)
        user.avatar = user_photo_path

    user.save()
