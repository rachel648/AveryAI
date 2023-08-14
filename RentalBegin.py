import csv

class Tenant:
    all = []

    def __init__(self,first_name: str, last_name: str, house_no,building_no = 0):
        self.first_name = first_name
        self.last_name = last_name
        self.house_no = house_no
        self.building_no = building_no

        # Adds instances to dict
        Tenant.all.append(self)


    @classmethod
    def instantiate_from_csv(cls):
        with open('tenants.csv', 'r') as f:
            reader = csv.DictReader(f)
            tenants = list(reader)
        for tenant in tenants:
            Tenant(
                first_name=tenant.get('first_name'),
                last_name=tenant.get('last_name'),
                house_no=tenant.get('house_no'),
                building_no=int(tenant.get('building_no')),
            )

    @staticmethod
    def is_integer(num):
        if isinstance(num,float):
            return num.is_integer()


    def __repr__(self):
        return f"Tenant('{self.first_name}', '{self.last_name}', {self.house_no}, {self.building_no})"


tenant1 = Tenant("Samson", "Moturi", "D1", 1004)



Tenant.instantiate_from_csv()
print(Tenant.all)
