from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones', '0003_candidacy_proposal_image_alter_candidacy_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidacy',
            old_name='proposal_image',
            new_name='profile_image',
        ),
    ]
