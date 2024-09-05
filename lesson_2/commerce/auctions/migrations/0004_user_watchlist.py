# Generated by Django 5.1 on 2024-09-03 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_listing_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlisted_by", to="auctions.listing"
            ),
        ),
    ]
