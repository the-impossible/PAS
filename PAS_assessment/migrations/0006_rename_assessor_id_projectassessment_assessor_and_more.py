# Generated by Django 4.1.5 on 2023-08-02 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("PAS_hallAllocation", "0001_initial"),
        ("PAS_assessment", "0005_seminarassessment_projectassessment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projectassessment", old_name="assessor_id", new_name="assessor",
        ),
        migrations.RenameField(
            model_name="projectassessment", old_name="student_id", new_name="student",
        ),
        migrations.RenameField(
            model_name="seminarassessment", old_name="assessor_id", new_name="assessor",
        ),
        migrations.RenameField(
            model_name="seminarassessment", old_name="student_id", new_name="student",
        ),
        migrations.AddField(
            model_name="projectassessment",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="PAS_hallAllocation.venue",
            ),
        ),
        migrations.AddField(
            model_name="seminarassessment",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="PAS_hallAllocation.venue",
            ),
        ),
    ]