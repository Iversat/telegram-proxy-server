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
git clone <ссылка на репозиторий >
cd telegram-proxy-server
docker compose build --no-cache
docker compose up -d
```
Управление пользователями:
Все команды управления выполняются через скрипт config.py внутри запущенного контейнера.
Добавление нового пользователя:
```bash
docker exec -it telegram-proxy-server python3 config.py add <имя_пользователя>
```
Просмотр списка пользователей:
```bash
docker exec -it telegram-proxy-server python3 config.py list
```
Получение ссылки для подключения (FakeTLS):
```bash
docker exec -it telegram-proxy-server python3 config.py link <имя_пользователя>
```
Управление доступом (Включение / Отключение)
Команды on и off позволяют временно приостановить или возобновить доступ пользователя. Изменение статуса вызывает мгновенную мягкую перезагрузку ядра MTProto, сбрасывая соединения отключенного юзера.
```bash
docker exec -it telegram-proxy-server python3 config.py off <имя_пользователя>
docker exec -it telegram-proxy-server python3 config.py on <имя_пользователя>
```
Полное удаление пользователя:
```bash
docker exec -it telegram-proxy-server python3 config.py del <имя_пользователя>
```
Структура проекта:
```bash
telegram-proxy-server/
├── docker-compose.yaml  — конфигурация для развертывания среды
├── Dockerfile           — инструкции для сборки Docker-образа
├── main.py              — процесс-менеджер для отслеживания базы и горячей перезагрузки
├── config.py            — панель управления пользователями и генератор секретов
├── users.enc            — зашифрованная база данных
└── .env                 — файл окружения с ключом шифрования и настройками
```
