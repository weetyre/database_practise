# Generated by Django 2.1.2 on 2018-12-17 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zone_manage', '0003_auto_20181218_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ainfo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bill',
            name='b_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='checkre',
            name='che_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='equip',
            name='equ_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hoster',
            name='hos_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='house',
            name='ho_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='worker',
            name='w_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
