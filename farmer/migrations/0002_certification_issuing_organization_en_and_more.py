# Generated by Django 4.2.19 on 2025-03-09 01:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("farmer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="certification",
            name="issuing_organization_en",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Issuing Organization",
            ),
        ),
        migrations.AddField(
            model_name="certification",
            name="issuing_organization_sq",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Organizata lëshuese",
            ),
        ),
        migrations.AddField(
            model_name="certification",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
        migrations.AddField(
            model_name="certification",
            name="name_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Emri"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
        migrations.AddField(
            model_name="crop",
            name="description_sq",
            field=models.TextField(blank=True, null=True, verbose_name="Përshkrimi"),
        ),
        migrations.AddField(
            model_name="crop",
            name="growing_season_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Growing Season"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="growing_season_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Sezoni i rritjes"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="name_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Emri"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="scientific_name_en",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Scientific Name"
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="scientific_name_sq",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Emri shkencor"
            ),
        ),
        migrations.AddField(
            model_name="cultivationmethod",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
        migrations.AddField(
            model_name="cultivationmethod",
            name="description_sq",
            field=models.TextField(blank=True, null=True, verbose_name="Përshkrimi"),
        ),
        migrations.AddField(
            model_name="cultivationmethod",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
        migrations.AddField(
            model_name="cultivationmethod",
            name="name_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Emri"
            ),
        ),
        migrations.AddField(
            model_name="farmerprofile",
            name="farm_description_en",
            field=models.TextField(
                blank=True, null=True, verbose_name="Farm Description"
            ),
        ),
        migrations.AddField(
            model_name="farmerprofile",
            name="farm_description_sq",
            field=models.TextField(
                blank=True, null=True, verbose_name="Përshkrimi i fermës"
            ),
        ),
        migrations.AddField(
            model_name="farmerprofile",
            name="farm_name_en",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Farm Name"
            ),
        ),
        migrations.AddField(
            model_name="farmerprofile",
            name="farm_name_sq",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Emri i fermës"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="address_en",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Address"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="address_sq",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Adresa"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="city_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="City"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="city_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Qyteti"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="country_en",
            field=models.CharField(
                blank=True,
                default="Albania",
                max_length=100,
                null=True,
                verbose_name="Country",
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="country_sq",
            field=models.CharField(
                blank=True,
                default="Shqipëri",
                max_length=100,
                null=True,
                verbose_name="Shteti",
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="region_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Region"
            ),
        ),
        migrations.AddField(
            model_name="farmlocation",
            name="region_sq",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Rajoni"
            ),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="activity_type_en",
            field=models.CharField(
                blank=True,
                choices=[
                    ("planting", "Mbjellje"),
                    ("fertilizing", "Plehërim"),
                    ("irrigating", "Ujitje"),
                    ("pest_control", "Kontroll i dëmtuesve"),
                    ("harvesting", "Vjelje"),
                    ("other", "Tjetër"),
                ],
                max_length=20,
                null=True,
                verbose_name="Activity Type",
            ),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="activity_type_sq",
            field=models.CharField(
                blank=True,
                choices=[
                    ("planting", "Mbjellje"),
                    ("fertilizing", "Plehërim"),
                    ("irrigating", "Ujitje"),
                    ("pest_control", "Kontroll i dëmtuesve"),
                    ("harvesting", "Vjelje"),
                    ("other", "Tjetër"),
                ],
                max_length=20,
                null=True,
                verbose_name="Lloji i aktivitetit",
            ),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="description_sq",
            field=models.TextField(blank=True, null=True, verbose_name="Përshkrimi"),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="notes_en",
            field=models.TextField(blank=True, null=True, verbose_name="Notes"),
        ),
        migrations.AddField(
            model_name="productionlog",
            name="notes_sq",
            field=models.TextField(blank=True, null=True, verbose_name="Shënime"),
        ),
    ]
