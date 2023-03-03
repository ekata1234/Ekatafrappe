import frappe

def validate(self,method = None):
    total_packaging=0
    for item in self.items:
        total_packaging = total_packaging + item.packaging_weight

    self.total_packaging = total_packaging
    self.total_net_weight = total_packaging + self.total_qty