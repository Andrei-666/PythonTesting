class ShippingCostCalculator:
    
    @staticmethod
    def calculate_cost(packages:list)->float:
        if len(packages)==0:
            raise ValueError("Lista de pachete nu poate fi goala.")
        
        total_cost=0.0

        for pkg in packages:
            weight = pkg['weight']
            distance = pkg['distance']
            is_fragile = pkg['is_fragile']
            if distance<=0 or weight<=0:
                raise ValueError("Distanta si greutatea trebuie sa fie mai mari decat 0.")
            
            if distance>1000:
                raise ValueError("Distanta introdusa depaseste limita acceptata (1000 km).")

            if weight>200:
                raise ValueError("Greutatea introdusa depaseste limita acceptata (200 kg).")
            
            if distance<5 and weight<5:
                base_cost=15.0
            else:
                base_cost=10.0+(1.0*distance)+max(0,2.0*(weight-2))
            
            if is_fragile:
                base_cost=base_cost*1.5
                                    
            total_cost+=base_cost
            
        return total_cost
