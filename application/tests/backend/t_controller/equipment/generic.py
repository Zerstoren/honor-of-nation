from tests.backend.t_controller.generic import Backend_Controller_Generic

from service.Equipment.Weapon import Service_Equipment_Weapon

class Backend_Controller_Equipment_Generic(Backend_Controller_Generic):

    def createEquipmentWeapon(self, user, wType='sword', damage=100, speed=40, critical_chance=5, critical_damage=2):
        service = Service_Equipment_Weapon()
        domain = service.save({
            'user': user.getId(),
            'type': wType,
            'damage': damage,
            'speed': speed,
            'critical_chance': critical_chance,
            'critical_damage': critical_damage
        }, user)

        return domain
