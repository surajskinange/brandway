# Generated to align the Blog model with the existing admin blog form.

from django.db import migrations, models
from django.utils.text import slugify


def populate_blog_slugs(apps, schema_editor):
    Blog = apps.get_model("accounts", "Blog")

    for blog in Blog.objects.all():
        base_slug = slugify(getattr(blog, "title", "") or "blog") or "blog"
        unique_slug = base_slug
        counter = 1

        while Blog.objects.filter(slug=unique_slug).exclude(id=blog.id).exists():
            counter += 1
            unique_slug = f"{base_slug}-{counter}"

        blog.slug = unique_slug
        blog.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_blog"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.RunPython(populate_blog_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="blog",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
