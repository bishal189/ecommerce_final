from django.core.management.base import BaseCommand
from django.apps import apps
import pandas as pd

class Command(BaseCommand):
    help= """ Import Data csv into django models
           usage:
           python manage.py import_product --path data.csv
           """



    def add_arguments(self,parser):   
        parser.add_argument('--path',type=str,help="file path",default='data.csv') 

    def handle(self,*args,**options):
        file_path=options['path']
        _model=apps.get_model('store','Product')
        df=pd.read_csv(file_path)
        df_records=df.to_dict('records')
        model_instances=[
            _model(

    # product_name=models.CharField(max_length=500)
    # slug=models.SlugField(max_length=200,unique=True)
    # description=models.TextField(max_length=500,blank=True)
    # images=models.ImageField(upload_to='photos/products')
    # stock=models.IntegerField()
    # price=models.IntegerField()
    # is_available=models.BooleanField(default=True)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)
    # created_date=models.DateTimeField(auto_now_add=True)
    # modified_at=models.DateTimeField(auto_now=True)
# product_name,description,stock,price,is_available,category
        product_name=record['product_name'],
        slug=record['slug']  ,
        description=record['description'],
        stock=record['stock'],
        price=record['price'],
        is_available=record['is_available'],      
        
        
        
        
        
        )
        for record in df_records
        ]

