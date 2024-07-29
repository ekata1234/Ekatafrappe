frappe.listview_settings['Attendance'] = {
    onload: function(listview) {
        // Check if the user has both "HR User" and "HR Manager" roles
        if (frappe.user.has_role('HR User') && frappe.user.has_role('HR Manager')) {
            console.log("hiii")
            // Hide the "Mark Attendance" button
            $('button[data-label="Mark%20Attendance"]').show();
        }
        else{
            console.log('hiiiiiiiii******')
            $('button[data-label="Mark%20Attendance"]').hide();
        }
    }
};