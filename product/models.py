from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from autoslug import AutoSlugField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
        Status = (
            ('True','Yes'),
            ('False','No'),
        )

        #id genareted automatically
        title=models.CharField(max_length=50)
        keywords=models.CharField(max_length=250)
        description=models.CharField(max_length=250)
        image=models.ImageField(blank=True,upload_to='CategoryImages/')
        statu=models.CharField(max_length=10,choices=Status)
        slug=AutoSlugField(populate_from='title')
        parent=TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)

        class MPTTMeta:
                order_insertion_by= ['title']

        def __str__(self):
                full_path=[self.title]
                k=self.parent
                while k is not None:
                        full_path.append(k.title)
                        k=k.parent
                return ' > '.join(full_path[::-1])


class Product(models.Model):
        Statu=(
                ('True','Yes'),
                ('False','No'),
        )

        category=models.ForeignKey(Category,on_delete=models.CASCADE)
        title=models.CharField(blank=True,max_length=50)
        keywords=models.CharField(blank=True,max_length=250)
        description=models.CharField(blank=True,max_length=250)
        image=models.ImageField(blank=True,upload_to='ProductImages/')
        price=models.FloatField()
        amount=models.IntegerField()
        ingredients=models.CharField(blank=True,max_length=150)
        detail=RichTextUploadingField(blank=True)
        statu=models.CharField(max_length=10,choices=Statu)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        slugTitle=AutoSlugField(populate_from='title',unique_with='created_at')
        slugCategory=AutoSlugField(populate_from='category')


        def __str__(self):
                return self.title

        def image_tag(self):
                return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

        image_tag.short_description= 'Image'

class Images(models.Model):

        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        title=models.CharField(max_length=50,blank=True)
        image=models.ImageField(blank=True,upload_to='ProductImages/')

        def __str__(self):
                return self.title

        def image_tag(self):
                return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

class Comment(models.Model):

        STATUS=(
                ('New','New'),
                ('True','True'),
                ('False','False'),
        )

        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        subject=models.CharField(max_length=50)
        comment=models.TextField(max_length=250)
        rate=models.IntegerField()
        status=models.CharField(max_length=10,choices=STATUS,default='New')
        ip=models.CharField(blank=True,max_length=20)
        create_at=models.DateTimeField(auto_now_add=True)
        update_at=models.DateTimeField(auto_now=True)

        def __str__(self):
                return self.subject

class CommentForm(ModelForm):
        class Meta:
                model = Comment
                fields= ['subject','comment','rate']