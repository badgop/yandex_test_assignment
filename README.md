UPDATE 07.05.2022
В настоящем репозитории находится мое решение тествого задания Yandex на вакансию "Разработчик-исследователь беспилотных автомобилей"  ( https://yandex.ru/jobs/vacancies/%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA-%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C-%D0%B1%D0%B5%D1%81%D0%BF%D0%B8%D0%BB%D0%BE%D1%82%D0%BD%D1%8B%D1%85-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9-400  )


_____________________________________________________________________

Настоящий каталог содержит файлы на языках Python и bash, которые необходимы для
демонстрации решения тестового задания. 

Описание решения - см. файл. "Описание решения задачи.odt"
Приложение отлажено на виртуальной машине с установленной ОС Ubuntu 20.04
Для развертывании окружения(установки утилит и библиотек для работы с CAN) следует последовательно запустить скрипты:
- install_script.sh
- pip.sh

Перед запуском и тестированием приложения следует запустить скрипт:
- create_vcans.sh
Настоящий скрипт загрузит модуль ядра vcan и создаст интерфейс "vcan0". Для проверки корректности работы следует просмотреть в терминале список интерфейсов, и убедиться что создан "vcan0"

Главный модуль разработанного приложения - bridge.py. 
Ключи запуска:
python3 bridge.py iphost port ipRealCanDev porti intname
где:
iphost - ip адрес хоста где будет запущено приложения. Для нужнд тестирования iphost = 'localhost'
port  - порт хоста для общения с RealCanDev (см. "Описание решения..." ). 
ipRealCanDev - ip адрес удаленого RealCanDe. Для нужд тестирования iphost = 'localhost'
porti - порт открытый на RealCanDev (см. "Описание решения..." ). porti!=port
intname  - имя интерфейса vcan. Для нужно тестирования intname  = 'vcan0'
Пример вызова: 
python3 bridge.py localhost 8000 localhost 8001 vcan0

Приложение для ручного тестирования - imitator.py
python3 bridge.py iphost port ipRealCanDev intname
описание ключей- аналогично. Следует запускать с теми же значениями.
Пример вызова: 
python3 imitator.py localhost 8000 localhost 8001 vcan0

Порядок запуска и тестирования:
- в отдельном окне терминала  запустить bridge.py
- в отдельном окне терминала  запустить imitator.py
- в отдельном окне терминала запустить candump
- в отдельном окне терминала выполнить команды:
cansend vcan0 $msg$
где msg - кадр CAN , например '134#DEADBEEF' или '5AA#'

В окне с candump появяться 2 строчки с одинаковым сообщением, которое было переслано через cansend

Разработал - Татарчук И.А. ivanttmtuci@gmail.com (telegram: @badgop) 