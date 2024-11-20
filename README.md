## Загрузчик изображений на Imgur

Простой загрузчик, позволяющий загружать изображения на Imgur через API и получать на них ссылки с тегами `[img][/img]`.
1. Установите Python c [официального сайта](https://www.python.org/downloads/)
2. Зарегистрируйтесь в Imgur API по [ссылке](https://api.imgur.com/oauth2/addclient) с параметрами:
   * Application Name - любое
   * Authorization type - Anonymous usage without user authorization
   * Authorization callback URL - `https://api.imgur.com/`
   * Введите ваш email и подтвердите капчу
3. Вы получите `client id` и `client secret`, для приложения понадобится только id - введите его в поле ввода. После первой загрузки введённый id сохранится в текстовый файл и в дальнейшем будет читаться оттуда.
