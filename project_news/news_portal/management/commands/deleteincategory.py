from django.core.management.base import BaseCommand, CommandError
from news_portal.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории'  # Подсказка вашей команды
    requires_migrations_checks = True  # Проверяет миграции

    def add_arguments(self, parser):
        # Добавляем аргумент для указания категории
        parser.add_argument('category', type=str, help='Категория, из которой требуется удалить новости')

    def handle(self, *args, **options):
        category_name = options['category']  # Получаем категорию из аргументов
        try:
            # Получаем объект категории по имени
            category = Category.objects.get(category_name=category_name)  # Исправлено на category_name
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('Категория не найдена. Убедитесь, что вы ввели корректное имя.'))
            return
        
        self.stdout.write(f'Вы собираетесь удалить все новости из категории: {category.category_name}.')
        self.stdout.write('Действительно хотите удалить все новости? да/нет')

        answer = input()  # Считываем подтверждение

        if answer.lower() == 'да':  # Проверяем подтверждение
            # Определяем количество статей, которые будут удалены
            posts_to_delete = Post.objects.filter(category=category)
            count_to_delete = posts_to_delete.count()  # Получаем количество статей для удаления

            if count_to_delete > 0:
                # Выводим информацию о количестве статей, которые будут удалены
                self.stdout.write(f'Найдено {count_to_delete} новостей для удаления.')
                posts_to_delete.delete()  # Удаляем все статьи из указанной категории
                self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории "{category.category_name}"!'))
            else:
                self.stdout.write(self.style.WARNING('Нет новостей для удаления.'))  # Если нет статей для удаления
        else:
            self.stdout.write(self.style.ERROR('Доступ запрещен. Удаление отменено.'))  # Если подтверждение неверно

