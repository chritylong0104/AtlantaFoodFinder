from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0004_alter_favorite_name_alter_favorite_place_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='name',
            field=models.CharField(default='Unnamed Favorite', max_length=255),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='place_id',
            field=models.CharField(default='default_place_id', max_length=255),
        ),
    ]
