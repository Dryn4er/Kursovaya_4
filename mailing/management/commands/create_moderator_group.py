from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создает группу модераторов и выдает необходимые права доступа'

    def handle(self, *args, **kwargs):
        # Создаем группу модераторов
        group_name = 'Moderators'
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))

        permissions = [
            'mailing.can_view_recipient_list',  # Замените на ваши права доступа
            'mailing.can_view_message_list',
            'mailing.can_stop_mailing',
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm.split('.')[-1])
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'Права "{perm}" добавлены в группу "{group_name}".'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Права "{perm}" не найдены.'))

        group.save()