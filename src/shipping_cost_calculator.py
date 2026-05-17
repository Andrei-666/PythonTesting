class ShippingCostCalculator:
    
    """
    
    SPECIFICATIA FUNCTIEI
    Functia shipping_cost_calculator.py calculeaza tariful total de livrare pentru o lista de pachete
    Intrari:
    -packages: o lista de dictionare, fiecare reprezentand un pachet cu "distance" (0<d<=1000), "weight" (0<w<=200) si "is_fragile" (bool)  
    -base_fee: un cost fix pentru coletele care nu depasesc niste praguri mici pentru distanta si greutate
    -fragile_multiplier: un multiplicator de cost pentru coletele fragile (+50% din cost)

    Iesiri:
    -float: pretul total calculat

    reguli:
    -se arunca ValueError daca lista este goala sau distanta/greutatea nu sunt in intervalul acceptat
    -daca distanta si greutatea sunt sub un anumit prag (<5 km/ <5 kg) se aplica un cost fix: base_fee=15.0
    -daca acestea sunt mai mari, se foloseste formula base_cost=10.0+(1.0*distance)+max(0,2.0*(weight-2))
    -daca pachetul este fragil, costul se inmulteste cu 1.5

"""


    @staticmethod
    def calculate_cost(packages:list,base_fee:float=15.0,fragile_multiplier:float=1.5)->float:
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
                base_cost=base_fee
            else:
                base_cost=10.0+(1.0*distance)+max(0,2.0*(weight-2))
            
            if is_fragile:
                base_cost=base_cost*fragile_multiplier
                                    
            total_cost+=base_cost
            
        return total_cost
