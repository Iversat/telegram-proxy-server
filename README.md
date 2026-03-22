# telegram-proxy-server
Markdown
# Telegram MTProto Proxy с FakeTLS

Высокопроизводительный MTProto прокси-сервер для Telegram, работающий в Docker-контейнере.

## Особенности
* **FakeTLS:** Маскировка трафика под обычные HTTPS-запросы (домен `vk.ru`) для обхода DPI.
* **Высокая скорость:** Использование `cryptg` и `gcc` для C-level ускорения криптографии.
* **Горячая перезагрузка (Hot-Reload):** Добавление, отключение и удаление пользователей на лету. Сервер подхватывает изменения без перезагрузки контейнера и обрыва текущих сессий.
* **Зашифрованная база:** Данные пользователей и секреты надежно хранятся в зашифрованном файле `users.enc`.

---

## Установка и запуск

```bash
git clone <ваш_репозиторий>
cd telegram-proxy-server
docker compose build --no-cache
docker compose up -d
Управление пользователями
Все команды управления выполняются через скрипт config.py внутри запущенного контейнера.

Добавление нового пользователя
Bash
docker exec -it telegram-proxy-server python3 config.py add <имя_пользователя>
Просмотр всех пользователей
Bash
docker exec -it telegram-proxy-server python3 config.py list
Получение FakeTLS-ссылки для подключения
Bash
docker exec -it telegram-proxy-server python3 config.py link <имя_пользователя>
Временное отключение и включение доступа
Bash
docker exec -it telegram-proxy-server python3 config.py off <имя_пользователя>
docker exec -it telegram-proxy-server python3 config.py on <имя_пользователя>
Полное удаление пользователя
Bash
docker exec -it telegram-proxy-server python3 config.py del <имя_пользователя>
Структура проекта
main.py — процесс-менеджер для отслеживания изменений базы и горячей перезагрузки MTProto.

config.py — панель управления пользователями и генератор секретов.

Dockerfile / docker-compose.yaml — конфигурации для сборки и развертывания среды.

users.enc — зашифрованная база данных.

.env — файл окружения с ключом шифрования и системными настройками.


Хочешь, я напишу для тебя файл `.gitignore`, чтобы ключи шифрования случайно не улетели в публичный репозиторий?
