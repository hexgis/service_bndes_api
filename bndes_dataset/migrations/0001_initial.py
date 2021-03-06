# Generated by Django 3.2 on 2022-07-14 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BNDESTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'BNDES Tag',
                'ordering': ('-tag',),
            },
        ),
        migrations.CreateModel(
            name='BNDESUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('service', models.CharField(max_length=255)),
                ('validity_in_days', models.IntegerField(default='15')),
                ('tags', models.ManyToManyField(related_name='urls', to='bndes_dataset.BNDESTag')),
            ],
            options={
                'verbose_name': 'BNDES url',
                'ordering': ('-url',),
            },
        ),
        migrations.CreateModel(
            name='BNDESLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.JSONField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('params', models.JSONField()),
                ('bndes_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bndes_url', to='bndes_dataset.bndesurl')),
            ],
            options={
                'verbose_name': 'BNDES Log',
                'ordering': ('date_created',),
            },
        ),
    ]
