import pandas as pd
from api.account.models import User, UserAddress
from api.core.models import Patient

from api.inventory.models import Medicine, MedicineCategory

print("Hello")

df = pd.read_csv("/home/arjun/Documents/project/skin_and_you/script/csv/patient.csv")

list_of_dict = df.to_dict('records')

UserAddress.objects.filter(user__email__icontains='patientfakeemail').delete()
Patient.objects.filter(user__email__icontains='patientfakeemail').delete()
User.objects.filter(email__icontains='patientfakeemail').delete()
# exit()

for medicine_dict in list_of_dict:
    
    serial_no = medicine_dict.get("Sr.no")
    patient_name = medicine_dict.get("Patients Name")
    medical_record_no = medicine_dict.get("Medical Record No.")
    age = medicine_dict.get("Age", 25)
    
    contact_no = medicine_dict.get("Contact Det.")
    email = medicine_dict.get("E-mail")
    consultant = medicine_dict.get("Consultant")
    address = medicine_dict.get("Address")
        
    # patient_first_name = patient_name.split(" ")[0]
    # patient_last_name = patient_name.split(" ")[0]
    
    if not patient_name:
        continue
        
    try:
        contact_no = contact_no.replace("+91", "")
        if "/" in contact_no:
            contact_no = contact_no[0]
    except:
        print("Excep 1")
        pass
    
    
    if email:
        email = "patientfakeemail."+str(contact_no)+"@gmail.com"
    
    # exit()
    try:
        user_obj = User(name=patient_name,email=email,mobile=contact_no,gender="Female")
        user_obj.save()
        
        print("User Id ", user_obj.id)
        
        
        # patient_obj = Patient(user_id=user_obj.id,branch_id='92e5580f-8448-44d3-bbe5-fd605723f4ba', age=age,medical_record_no=medical_record_no)
        # patient_obj.save()
        
        # user_address_obj = UserAddress(user_id=user_obj.id, address=address,pincode=400001,city_id='390fe318-5219-47ea-910b-bd03a7548b63',state_id='11dbe29c-770d-4737-a87d-7a5309b2ba58')
        # user_address_obj.save()
    
        patient_obj = Patient(user_id=user_obj,branch_id='2d9b7622-3460-477e-ba9f-31455bb5b35a', age=age,medical_record_no=medical_record_no)
        patient_obj.save()
        
        user_address_obj = UserAddress(user_id=user_obj, address=address,pincode=400001,city_id='43439168-03eb-4b3e-928d-9e5a81d36767',state_id='e8a5a3c2-fd3f-419c-ab01-41aa7dadf5b8')
        user_address_obj.save()
    except:
        print("===")
        