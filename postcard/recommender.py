import redis
from django.conf import settings
from .models import Postcard

# Соединение с Redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:
    def get_postcard_key(self, id):
        return f'postcard:{id}:purchased_with'

    def postcard_buy(self, postcards):
        postcard_ids = [p.id for p in postcards]
        for postcard_id in postcard_ids:
            for with_id in postcard_ids:
                # Получение других открыток, купленных вместе с текущей
                if postcard_id != with_id:
                    r.zincrby(self.get_postcard_key(postcard_id),
                              1, with_id)

    def offer_postcard_for(self, postcards, max_results=6):
        postcard_ids = [p.id for p in postcards]
        if len(postcards) == 1:
            # Если только 1 открытка
            offers = r.zrange(self.get_postcard_key(postcard_ids[0]),
                              0, -1, desc=True)[:max_results]
        else:
            # Сгенерировать временный ключ
            flat_ids = ''.join([str(id) for id in postcard_ids])
            tmp_key = f'tmp_{flat_ids}'
            # несколько открыток, объединить баллы всех открыток
            # сохранить полученное сортированное множество во временном ключе
            keys = [self.get_postcard_key(id) for id in postcard_ids]
            r.zunionstore(tmp_key, keys)
            # удалить идентификаторы открыток,
            # для которых дается рекомендация
            r.zrem(tmp_key,*postcard_ids)
            # получить идентификаторы открыток по их количеству,
            # сортировка по убыванию
            offers = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)  # удалить временный ключ
        offers_postcards_ids = [int(id) for id in offers]
        # получить предлагаемые открытки и
        # отсортировать их по порядку их появления
        offers_postcards = list(Postcard.objects.filter(
            id__in=offers_postcards_ids))
        offers_postcards.sort(key=lambda x: offers_postcards_ids.index(x.id))
        return offers_postcards

    def clear_purchases(self):
        #  Очистка рекомендаций
        for id in Postcard.objects.values_list('id', flat=True):
            r.delete(self.get_postcard_key(id))
