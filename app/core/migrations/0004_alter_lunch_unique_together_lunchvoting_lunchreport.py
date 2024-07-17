# Generated by Django 4.2 on 2024-07-17 10:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_lunch'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lunch',
            unique_together={('user', 'day')},
        ),
        migrations.CreateModel(
            name='LunchVoting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('lunch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.lunch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lunch Voting',
                'verbose_name_plural': 'Lunch Voting',
                'unique_together': {('user', 'date')},
            },
        ),
        migrations.CreateModel(
            name='LunchReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.SmallIntegerField(default=0)),
                ('lunch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.lunch')),
            ],
            options={
                'verbose_name': 'Lunch Report',
                'verbose_name_plural': 'Lunch Reports',
                'unique_together': {('lunch', 'date')},
            },
        ),
    ]