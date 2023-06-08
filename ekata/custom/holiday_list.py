
import frappe
from datetime import datetime, timedelta
from frappe.model.document import Document


@frappe.whitelist()
def send_notifications_mail():
    print("\n\n ----in mail---\n\n")
    # Get the current date
    current_date = datetime.now().date()
    print("\n\n ----cur_date---",current_date)
    # Calculate the date 1 day before
    target_date = current_date + timedelta(days=1)
    print("\n\n ----tar_date---",target_date)


    # Retrieve the relevant documents or events that match the target date
    holiday_list = frappe.db.get_list('Holiday',filters={'holiday_date': target_date},fields=['description','holiday_date'])
    emp_list = frappe.db.get_list('Employee',filters={'status': 'Active'},fields=['prefered_email','employee_name'])
    print("\n\n ----holiday_list1---",holiday_list)
    print("\n\n ----emp_list---",emp_list)

    attendee_email =[]
    for emp in emp_list:
        if emp.prefered_email != None:
            attendee_email.append(emp.prefered_email)
    print("\n\n ----emp_list mail---",attendee_email)
    

    # Iterate through the events and send email notifications
   for holiday in holiday_list:
        print("\n holiday dt--",holiday)
        for emp in attendee_email:
            for mail in emp_list:
                print("\n emp--",emp)
                subject = f"Reminder:  '{holiday.description}' is tomorrow"
                
                recipients = emp            
                message = f"Dear {mail.employee_name}! This email is to remind you about the upcoming holidays.\n\n Below is the list of upcoming holidays for you:\n'{holiday.description}'"
                
                # Send the email using the frappe library
                print(f"\n\n #####{subject}\n{recipients}\n{message}\n")
                frappe.sendmail(recipients=recipients, subject=subject, message=message)

