from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.db.backends.signals import connection_created

        def configure_sqlite(sender, connection, **kwargs):
            if connection.vendor == 'sqlite':
                with connection.cursor() as cursor:
                    cursor.execute('PRAGMA journal_mode = WAL;')
                    cursor.execute('PRAGMA synchronous = NORMAL;')
                    cursor.execute('PRAGMA busy_timeout = 30000;')

        connection_created.connect(configure_sqlite)
