### Фильтрация продуктов

 - позволяет заблокировать продукт, отправив имя поля и значение(у продукта) по которому блокировать в топик 'blocked_teg_products'
 - после чего эта информация добаляется в 'blocked_product_table'
 - теперь при публикации продукта в 'publish_products' faust проверяет его и если нет блокировки отправляет в топик 'filtered_products'

### Start

 - Запустите приложение faust `faust -A faust_main worker -l info`
 - для загрузки тестовых данных для блокировки запустите `python3 producer_for_block_product.py`
 - для загрузки тестовых продуктов запустите `python producer.py`