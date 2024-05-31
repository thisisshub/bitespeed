from .models import Contact

def get_identify_response(id):
    """
    Get the consolidated contacts for customer whose primaryID is "id"
    """
    primary_instance = Contact.objects.get(id=id)
    email_list, phone_list, sec_contact_ids = _collect_contact_details(primary_instance)
    
    response = {
        "contact": {
            "primaryContactId": id,
            "emails": email_list,
            "phoneNumbers": phone_list,
            "secondaryContactIds": sec_contact_ids
        }
    }
    return response

def _collect_contact_details(primary_instance):
    """
    Helper function to collect contact details of primary and linked instances.
    """
    email_list = [primary_instance.email] if primary_instance.email else []
    phone_list = [primary_instance.phoneNumber] if primary_instance.phoneNumber else []
    sec_contact_ids = []

    queryset = Contact.objects.filter(linkedId=primary_instance.id)
    for instance in queryset:
        sec_contact_ids.append(instance.id)
        if instance.email and instance.email not in email_list:
            email_list.append(instance.email)
        if instance.phoneNumber and instance.phoneNumber not in phone_list:
            phone_list.append(instance.phoneNumber)
    
    return email_list, phone_list, sec_contact_ids

def combine(old_id, new_id):
    """
    Link all the new_id contacts to old_id
    """
    queryset = Contact.objects.filter(linkedId=new_id)
    for instance in queryset:
        instance.linkedId_id = old_id
        instance.save()
    
    parent_instance = Contact.objects.get(id=new_id)
    parent_instance.linkedId_id = old_id
    parent_instance.linkPrecedence = "secondary"
    parent_instance.save()

def combine_customers(email, phoneNumber):
    """
    Combine two different customers using email of one customer with phoneNumber of the other and return older instance
    """
    email_instance = Contact.objects.filter(email=email).first()
    phone_instance = Contact.objects.filter(phoneNumber=phoneNumber).first()

    primary_email_instance_id = _get_primary_instance_id(email_instance)
    primary_phone_instance_id = _get_primary_instance_id(phone_instance)

    if primary_email_instance_id != primary_phone_instance_id:
        if primary_email_instance_id < primary_phone_instance_id:
            combine(primary_email_instance_id, primary_phone_instance_id)
            return primary_email_instance_id
        else:
            combine(primary_phone_instance_id, primary_email_instance_id)
            return primary_phone_instance_id
    
    return primary_email_instance_id

def _get_primary_instance_id(instance):
    """
    Helper function to get the primary instance ID for a given contact instance.
    """
    if instance.linkPrecedence == "secondary":
        return instance.linkedId_id
    return instance.id
