import pandas as pd

from api.inventory.models import Medicine, MedicineCategory

print("Hello")

df = pd.read_csv("/home/arjun/Documents/project/skin_and_you/script/csv/medicine.csv")

list_of_dict = df.to_dict('records')

for medicine_dict in list_of_dict:
    serial_no = medicine_dict.get("Sr. No")
    category = medicine_dict.get("Medicine Category")
    product_name = medicine_dict.get("Medicine Name")
    content = medicine_dict.get("Content")
    sku_code = medicine_dict.get("SKU Code")
    print("sku_code ", sku_code)
    
    # sku_code = str(category).replace(" ", "_").upper() + "_" + str(serial_no)
    
    try:
        category_list = MedicineCategory.objects.filter(name=str(category).title())
        if category_list:
            category_obj = category_list[0]
        else:
            category_obj = MedicineCategory(name=str(category).title())
            category_obj.save()
            
        if product_name:
            
            medicine_obj = Medicine(
                medicine_category=category_obj, 
                sku_code=sku_code,
                name=str(product_name).title(),
                content=str(content).title(),
                serial_number=serial_no,
                price=0
            )    
            medicine_obj.save()
            
        print(category_obj.id)
    except:
        print("Already exist")