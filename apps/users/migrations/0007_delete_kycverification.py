

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merge_20251121_2008'),
    ]

    operations = [
        migrations.DeleteModel(
            name='KYCVerification',
        ),
    ]
