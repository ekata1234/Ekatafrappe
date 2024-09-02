import frappe
from frappe.utils import now_datetime, time_diff_in_hours,pretty_date, now, add_to_date
from datetime import datetime, date
from email.utils import formataddr

def delete_email_queues():
    # '''method deletes email queues whose status is in Sent and/or Error'''
    
    #checking the day of the week, the script only works on monday, wednesday and friday
    # if not frappe.utils.get_datetime().weekday() in [1,3,5,6]:
    c = str(now_datetime())[11:13]
    d = int(c)
    a = "1"
    b = int(a)
    if frappe.utils.get_datetime().weekday() in [0,1,2,3,4,5,6] and d == b:

        print("\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n")
        #getting the tuple of names of Email Queues with status in Sent or Error
        deletable_email_queues_tuple = frappe.db.sql('''
        SELECT
            name
        FROM
            `tabEmail Queue`
        WHERE
            status
        IN
            ('Sent', 'Error','Expired')
        ''')
            
            #deleting the email queues in safe update mode
        frappe.db.sql('''
        DELETE FROM
            `tabEmail Queue`
        WHERE
            name
        IN
            %(deletable_email_queues)s;
        ''', values={'deletable_email_queues':deletable_email_queues_tuple})

        print("\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\ns")