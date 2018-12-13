# Generated by Django 2.1.2 on 2018-12-13 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AInfo',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('inf_time', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'a_info',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('b_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('b_name', models.CharField(blank=True, max_length=20, null=True)),
                ('b_amount', models.FloatField(blank=True, null=True)),
                ('b_date', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'bill',
            },
        ),
        migrations.CreateModel(
            name='CheckRe',
            fields=[
                ('che_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date_ch', models.DateField(auto_now_add=True, null=True)),
                ('worktime', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'check_re',
            },
        ),
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('equ_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('buy_date', models.DateField(auto_now_add=True, null=True)),
                ('loca', models.CharField(blank=True, max_length=20, null=True)),
                ('fix_date', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'equip',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('exp_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('duty_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('amount', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'expense',
            },
        ),
        migrations.CreateModel(
            name='Hoster',
            fields=[
                ('hos_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('contact', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('bonus', models.BigIntegerField(blank=True, null=True)),
                ('coupon_nam', models.CharField(blank=True, max_length=8, null=True)),
                ('pass_field', models.BigIntegerField(blank=True, db_column='pass', null=True)),
                ('loign_nam', models.CharField(blank=True, max_length=8, null=True)),
                ('hos_name', models.CharField(blank=True, max_length=8, null=True)),
                ('sex', models.CharField(blank=True, max_length=4, null=True)),
                ('in_time', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'hoster',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('ho_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('area', models.FloatField(blank=True, null=True)),
                ('unit_n', models.BigIntegerField(blank=True, null=True)),
                ('avi', models.BigIntegerField(blank=True, null=True)),
                ('bel_name', models.CharField(blank=True, max_length=10, null=True)),
                ('pub_area', models.FloatField(blank=True, null=True)),
                ('bel_id', models.BigIntegerField(blank=True, null=True)),
                ('flour', models.BigIntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('rent', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'house',
            },
        ),
        migrations.CreateModel(
            name='InOut',
            fields=[
                ('log_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('guest_name', models.CharField(blank=True, max_length=8, null=True)),
                ('indate', models.DateField(blank=True, null=True)),
                ('outdate', models.DateField(blank=True, null=True)),
                ('contact', models.BigIntegerField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'in_out',
            },
        ),
        migrations.CreateModel(
            name='ParLot',
            fields=[
                ('par_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('gar_num', models.BigIntegerField()),
                ('rent', models.FloatField(blank=True, null=True)),
                ('avi', models.BigIntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'par_lot',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('change_date', models.DateField(auto_now=True, null=True)),
                ('type_field', models.BigIntegerField(blank=True, db_column='type_', null=True)),
                ('crea_time', models.DateField(auto_now_add=True, null=True)),
                ('content_field', models.CharField(blank=True, db_column='content_', max_length=200, null=True)),
                ('rule_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'rule_',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('sa_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('base_sal', models.FloatField(blank=True, null=True)),
                ('handout_time', models.DateField(blank=True, null=True)),
                ('up_sa', models.FloatField(blank=True, null=True)),
                ('secu_sa', models.FloatField(blank=True, null=True)),
                ('deduct', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'salary',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('w_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('work_area', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, max_length=4, null=True)),
                ('in_date', models.DateField(auto_now_add=True, null=True)),
                ('work_time', models.FloatField(blank=True, null=True)),
                ('type', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'worker',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('sex', models.CharField(max_length=10, null=True, verbose_name='sex')),
                ('type', models.IntegerField(null=True, verbose_name='type')),
                ('created_at', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'myuser',
            },
        ),
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('workid', models.ForeignKey(db_column='workid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Zone_manage.Worker')),
                ('content_field', models.CharField(blank=True, db_column='content_', max_length=200, null=True)),
                ('reco_time', models.DateField(auto_now_add=True, null=True)),
                ('state', models.BigIntegerField(blank=True, null=True)),
                ('type_re', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'advice',
            },
        ),
        migrations.CreateModel(
            name='Fix',
            fields=[
                ('workid', models.ForeignKey(db_column='workid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Zone_manage.Worker')),
                ('date_field', models.DateField(auto_now=True, db_column='date_', null=True)),
                ('equ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Equip')),
            ],
            options={
                'db_table': 'fix',
            },
        ),
        migrations.CreateModel(
            name='Look',
            fields=[
                ('hoster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Zone_manage.Hoster')),
                ('date_field', models.DateField(auto_now=True, db_column='date_', null=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.AInfo')),
            ],
            options={
                'db_table': 'look',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Zone_manage.Worker')),
                ('date_field', models.DateField(auto_now=True, db_column='date_', null=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.AInfo')),
            ],
            options={
                'db_table': 'operation',
            },
        ),
        migrations.CreateModel(
            name='Uses',
            fields=[
                ('hoster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Zone_manage.Hoster')),
                ('date_field', models.DateField(auto_now=True, db_column='date_', null=True)),
                ('equ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Equip')),
            ],
            options={
                'db_table': 'uses',
            },
        ),
        migrations.AddField(
            model_name='salary',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='rule',
            name='crea_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='parlot',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Hoster'),
        ),
        migrations.AddField(
            model_name='parlot',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='inout',
            name='hoster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Hoster'),
        ),
        migrations.AddField(
            model_name='inout',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='house',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Hoster'),
        ),
        migrations.AddField(
            model_name='house',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='expense',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='checkre',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AddField(
            model_name='bill',
            name='hoster_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Hoster'),
        ),
        migrations.AddField(
            model_name='bill',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Worker'),
        ),
        migrations.AlterUniqueTogether(
            name='parlot',
            unique_together={('par_id', 'gar_num')},
        ),
        migrations.AddField(
            model_name='advice',
            name='hoster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zone_manage.Hoster'),
        ),
        migrations.AlterUniqueTogether(
            name='uses',
            unique_together={('hoster', 'equ')},
        ),
        migrations.AlterUniqueTogether(
            name='operation',
            unique_together={('worker', 'log')},
        ),
        migrations.AlterUniqueTogether(
            name='look',
            unique_together={('hoster', 'log')},
        ),
        migrations.AlterUniqueTogether(
            name='fix',
            unique_together={('workid', 'equ')},
        ),
        migrations.AlterUniqueTogether(
            name='advice',
            unique_together={('workid', 'hoster')},
        ),
    ]
