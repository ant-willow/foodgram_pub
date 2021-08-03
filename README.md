# foodgram-project
![foodgram workflow](https://github.com/ant-willow/foodgram_pub/workflows/foodgram%20workflow/badge.svg)

## Продуктовый помощник
Это онлайн-сервис, где пользователи смогут публиковать рецепты,\
подписываться на публикации других пользователей,\
добавлять понравившиеся рецепты в список «Избранное»,\
а перед походом в магазин скачивать сводный список продуктов,\
необходимых для приготовления одного или нескольких выбранных блюд.

## Инструкция для развертывания:
 - Клонировать себе репозиторий
 - Заполнить секреты в репозитории:\
	 **USER** - имя пользователя для подключения к серверу\
	 **HOST** - IP-адрес сервера\
	 **SSH_KEY** - приватный ключ\
	 **PASSPHRASE** - фраза-пароль для ключа\
	 **DOCKER_USERNAME** - имя пользователя Docker Hub\
	 **DOCKER_PASSWORD** - пароль от Docker Hub\
	 **SECRET_KEY** - секретный ключ Django\
	 **POSTGRES_PASSWORD** - пароль от базы\
	 **DOMAIN_NAME** - доменное имя сайта
 - Сделать push

После удачного запуска, проект будет доступен по адресу HOST

([foodgram](http://foodgra.ml))
