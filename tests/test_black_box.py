import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
--------------------------------------------------------------------------------------------------------------
SPECIFICATIA FUNCTIEI
Functia def calculate_cost(packages:list,base_fee:float=15.0,fragile_multiplier:float=1.5) calculeaza tariful total de livrare pentru o lista de pachete

Intrari:
    -packages: o lista de dictionare, fiecare reprezentand un pachet cu "distance" (0<distance<=1000), "weight" (0<weight<=200) si "is_fragile" (bool)  
    -base_fee: un cost fix pentru coletele care nu depasesc niste praguri mici pentru distanta si greutate
    -fragile_multiplier: un multiplicator de cost pentru coletele fragile (+50% din cost)

Iesiri:
    -float: pretul total calculat
   

Reguli:
    -se arunca ValueError daca lista este goala sau distanta/greutatea nu sunt in intervalul acceptat
    -daca distanta si greutatea sunt sub un anumit prag (<5 km/ <5 kg) se aplica un cost fix: base_fee=15.0
    -daca acestea sunt mai mari, se foloseste formula base_cost=10.0+(1.0*distance)+max(0,2.0*(weight-2))
    -daca pachetul este fragil, costul se inmulteste cu fragile_multiplier=1.5
    

-------------------------------------------------------------------------------------------------------------------------------------

                                    Teste black box 


------------partitionare de echivalenta si analiza valorilor de frontiera-----------------


1. Domeniul de intrari. Avem 4 intrari
-lista de pachete (packages)
-distanta de livrare (distance)
-greutatea coletului (weight)
-optiunea care indica daca pachetul este fragil (is_fragile)


-packages poate fi:
    L_1= lista nevida de pachete
    L_2= lista goala

-distance trebuie sa fie in intervalul (0,1000], iar pragul 5 separa zona de cost fix de zona de calcul prin formula, deci se disting 4 clase de echivalenta:
    D_1={d | 0<d<5}
    D_2={d | 5<=d<=1000}
    D_3={d | d<=0}
    D_4={d | d>1000}

-weight trebuie sa fie in intervalul (0,200],iar pragul 5 separa zona de cost fix de zona de calcul prin formula,deci se disting 4 clase de echivalenta:
    W_1={w | 0<w<5}
    W_2={w | 5<=w<=200}
    W_3={w | w<=0}
    W_4={w | w>200}

-is_fragile este o optiune binara,deci se disting 2 clase de echivalenta:
    F_1={False}
    F_2={True}

    
2. Domeniul de iesiri:
-cost fix pentru pachetele cu distanta si greutate sub pragul 5
-cost calculat prin formula pentru restul pachetelor valide
-cost multiplicat daca pachetul este fragil
-eroare pentru date invalide


3. Clasele de echivalenta globale

Clasele de echivalenta pentru intregul program se pot obtine ca o combinatie a claselor individuale:

C_1={(l,d,w,f) | l->L_1, d->D_1, w->W_1, f->F_1} //cost fix, nefragil
C_2={(l,d,w,f) | l->L_1, d->D_1, w->W_1, f->F_2} //cost fix, fragil
C_3={(l,d,w,f) | l->L_1, d->D_2, w->W_2, f->F_1} //formula standard, nefragil (distanta mare, greutate mare)
C_4={(l,d,w,f) | l->L_1, d->D_2, w->W_2, f->F_2} //formula standard, fragil
C_5={(l,d,w,f) | l->L_1, d->D_2, w->W_1, f->F_1} //formula standard, distanta mare, greutate mica
C_6={(l,d,w,f) | l->L_1, d->D_1, w->W_2, f->F_1} //formula standard, distanta mica, greutate mare
C_7={(l) | l contine mai multe pachete valide} //mai multe pachete valide
C_8={(l,d,w,f) | l->L_2} //lista goala
C_9={(l,d,w,f) | l->L_1, d->D_3} //distance<=0
C_10={(l,d,w,f) | l->L_1, d->D_4} //distance>1000
C_11={(l,d,w,f) | l->L_1, w->W_3} //weight<=0
C_12={(l,d,w,f) | l->L_1, w->W_4} //weight>200
C_13={(l) | l contine cel putin un pachet invalid} //lista cu pachet invalid


4. Setul de date:

c_1: ([(2,2,F)])
c_2: ([(2,2,T)])
c_3: ([(10,5,F)])
c_4: ([(10,5,T)])
c_5: ([(50,1,F)])
c_6: ([(2,10,F)])
c_7: ([(2,2,F),(10,5,F),(10,5,T)])
c_8: ([])
c_9a: ([(-10,5,F)])
c_9b: ([(0,5,F)])
c_10: ([(1500,5,F)])
c_11a: ([(10,-1,F)])
c_11b: ([(10,0,F)])
c_12: ([(10,250,F)])
c_13: ([(10,5,F),(-1,5,F),(10,5,F)])

Intrari                 Rezultat afisat(expected)
l,d,w,f

[(2,2,F)]                                    15.0
[(2,2,T)]                                    22.5
[(10,5,F)]                                   26.0
[(10,5,T)]                                   39.0
[(50,1,F)]                                   60.0
[(2,10,F)]                                   28.0
[(2,2,F),(10,5,F),(10,5,T)]                  80.0
[]                                           ValueError
[(-10,5,F)]                                  ValueError
[(0,5,F)]                                    ValueError
[(1500,5,F)]                                 ValueError
[(10,-1,F)]                                  ValueError
[(10,0,F)]                                   ValueError
[(10,250,F)]                                 ValueError
[(10,5,F),(-1,5,F),(10,5,F)]                 ValueError
"""



class TestEquivalencePartitioning:  

    #invalid list --------------------------------------------
    #c_8: ([]), lista goala
    def test_equivalence_partitioning_empty_packages(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #invalid distance ------------------------------------------------

    #distanta <0
    #c_9a: ([(-10,5,F)]), distance<0
    def test_equivalence_partitioning_negative_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': -10, 'weight': 5, 'is_fragile': False}])

    #distanta = 0
    #c_9b: ([(0,5,F)]), distance=0
    def test_equivalence_partitioning_zero_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 0, 'weight': 5, 'is_fragile': False}])

    #distanta>1000 (limita)
    #c_10: ([(1500,5,F)]), distance>1000
    def test_equivalence_partitioning_distance_above_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 1500, 'weight': 5, 'is_fragile': False}])


    #invalid weight---------------------------------------------------

    #greutatea <0 
    #c_11a: ([(10,-1,F)]), weight<0
    def test_equivalence_partitioning_negative_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': -1, 'is_fragile': False}])

    #greutatea=0
    #c_11b: ([(10,0,F)]), weight=0
    def test_equivalence_partitioning_zero_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 0, 'is_fragile': False}])

    #greutatea>200 (limita)
    #c_12: ([(10,250,F)]), weight>200
    def test_equivalence_partitioning_weight_above_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 250, 'is_fragile': False}])




    #fixed cost -------------------------------------------------------------

    """fixed cost-basic package"""

    #costul fix (greutate si distanta mici); nefragil
    #c_1: ([(2,2,F)]), cost fix nefragil
    def test_equivalence_partitioning_fixed_cost_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 2, 'is_fragile': False}])==pytest.approx(15.0)

    #costul fix (greutate si distanta mici); fragil
    #c_2: ([(2,2,T)]), cost fix fragil
    def test_equivalence_partitioning_fixed_cost_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 2, 'is_fragile': True}])==pytest.approx(22.5)



    #standard formula ---------------------------------------------------------------------

    """formula"""

    #pachet normal, nefragil = 10+10+max(0,2*(5-2))
    #c_3: ([(10,5,F)]), formula standard nefragil (distanta mare, greutate mare)
    def test_equivalence_partitioning_standard_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 5, 'is_fragile': False}])==pytest.approx(26.0)

    #pachet normal fragil = nefragil*1.5
    #c_4: ([(10,5,T)]), formula standard fragil
    def test_equivalence_partitioning_standard_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 5, 'is_fragile': True}])==pytest.approx(39.0)

    #colet usor, sub 2kg, fara penalizare pe greutate
    #c_5: ([(50,1,F)]), formula standard, distanta mare, greutate mica
    def test_equivalence_partitioning_below_penalty_light(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 50, 'weight': 1, 'is_fragile': False}])==pytest.approx(60.0)

    #colet greu, distanta mica
    #c_6: ([(2,10,F)]), formula standard, distanta mica, greutate mare = 10+(1.0*2)+2*(10-2)
    def test_equivalence_partitioning_formula_short_distance_heavy_weight(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 10, 'is_fragile': False}])==pytest.approx(28.0)

    #colet greu, peste 2kg, cu penalizare pe greutate
    #c_3: ([(100,100,F)]), validare suplimentara pt formula standard
    def test_equivalence_partitioning_above_penalty_heavy(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 100, 'weight': 100, 'is_fragile': False}])==pytest.approx(306.0)


    #multiple packages -----------------------------------------------------
    #c_7: ([(2,2,F),(10,5,F),(10,5,T)]), mai multe pachete valide
    def test_equivalence_partitioning_multiple_packages(self):
        #fixed cost+formula+fragile=15+26+39=80
        packages = [
                {'distance': 2,  'weight': 2, 'is_fragile': False},
                {'distance': 10, 'weight': 5, 'is_fragile': False},
                {'distance': 10, 'weight': 5, 'is_fragile': True},
            ]
        assert ShippingCostCalculator.calculate_cost(packages)==pytest.approx(80.0)


    #c_13: ([(10,5,F),(-1,5,F),(10,5,F)]), lista cu pachet invalid
    def test_equivalence_partitioning_invalid_package_in_middle(self):

        packages = [
            {'distance': 10, 'weight': 5,   'is_fragile': False},
            {'distance': -1, 'weight': 5,   'is_fragile': False},
            {'distance': 10, 'weight': 5,   'is_fragile': False},
        ]
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(packages)


class TestBoundaryValueAnalysis:
    """boundary limits-----------------------------------------------------------------------------------------------------------------------
    
    
    2.Valori de frontiera
    distanta: 0(invalid), 0.01(minim valid), 4.99(sub limita de base cost), 5.0(pe limita de la formula), 1000(maxim valid), 1000.01 (invalid)
    greutatea: 0(invalid), 0.01(minim valid), 2.0(pe limita de la formula), 4.99(sub limita de base cost), 5.0(pe limita de base cost), 200(maxim valid), 200.01(invalid)

-distanta:
    D_1: 0, 0.01 //limita inferioara
    D_2: 4.99, 5.0, 5.01 //pragul de schimbare a formulei
    D_3: 1000, 1000.01

-weight:
    W_1: 0 //limita inferioara
    W_2: 1.99, 2.0, 2.01 //pragul de penalizare greutate
    W_3: 4.99, 5.0 //prag de schimbare a formulei de cost fix
    W_4: 200, 200.01 //limita superioara

-liste:
    0, 1 sau >1 elemente

-fragil:
    True, False

Setul de date de test
B_1: ([(0,5,F)])
B_2: ([(0.01,5,F)])
B_3: ([(4.99,1,F)])
B_4: ([(5.0,3,F)])
B_5: ([(5.01,1,F)])
B_6: ([(1,4.99,F)])
B_7: ([(1,5.0,F)])
B_8: ([(10,1.99,F)])
B_9: ([(10,2.0,F)])
B_10: ([(10,2.01,F)])
B_11: ([(1000,2,F)])
B_12: ([(1000.01,2,F)])
B_13: ([(10,200,F)])
B_14: ([(10,200.01,F)])
B_15: ([(1000,200,T)])
B_16: ([(4.99,4.99,T)])
B_17: ([(2,2,F),(10,5,F)])
B_18: ([(10,5,F),(10,201,F)])



Intrari                                         Rezultat afisat (expected)
l, d, w, f

[(0, 5, F)]                                     ValueError 
[(0.01, 5, F)]                                  16.01          
[(4.99, 1, F)]                                  15.0          
[(5.0, 3, F)]                                   17.0          
[(5.01, 1, F)]                                  15.01          
[(1, 4.99, F)]                                  15.0           
[(1, 5.0, F)]                                   17.0           
[(10, 1.99, F)]                                 20.0           
[(10, 2.0, F)]                                  20.0           
[(10, 2.01, F)]                                 20.02          
[(1000, 2, F)]                                  1010.0        
[(1000.01, 2, F)]                               ValueError     
[(10, 200, F)]                                  416.0          
[(10, 200.01, F)]                               ValueError     
[(1000, 200, T)]                                2109.0         
[(4.99, 4.99, T)]                               22.5           
[(2,2,F),(10,5,F)]                              41.0
[(10,5,F),(10,201,F)]                           ValueError
"""

    


    # B_1: distanta = 0 (invalid)
    def test_boundary_zero_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 0, 'weight': 5, 'is_fragile': False}])

    # B_2: distanta = 0.01, greutatea = 5 valid, imediat peste limita de 0
    def test_boundary_minimum_valid_formula(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 0.01, 'weight': 5, 'is_fragile': False}]) == pytest.approx(16.01)

    # B_3: distanta = 4.99 (sub limita de 5 din formula - pret fix)
    def test_boundary_distance_below_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 4.99, 'weight': 1, 'is_fragile': False}]) == pytest.approx(15.0)

    # B_4: distanta = 5.0 (exact pe limita de 5 din formula - trece la pret calculat)
    def test_boundary_distance_on_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 5.0, 'weight': 3, 'is_fragile': False}]) == pytest.approx(17.0)

    # B_5: distanta = 5.01 (imediat peste limita de 5 din formula - pret calculat)
    def test_boundary_distance_above_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 5.01, 'weight': 1, 'is_fragile': False}]) == pytest.approx(15.01)

    # B_6: greutatea = 4.99 (sub limita de 5 din formula - pret fix)
    def test_boundary_weight_below_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1, 'weight': 4.99, 'is_fragile': False}])==pytest.approx(15.0)

    # B_7: greutatea = 5.0 (egala cu limita de 5 din formula - pret calculat)
    def test_boundary_weight_on_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1, 'weight': 5.0, 'is_fragile': False}]) == pytest.approx(17.0)

    # B_8: greutatea = 1.99 (imediat sub penalizarea de limita 2kg)
    def test_boundary_weight_below_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 1.99, 'is_fragile': False}]) == pytest.approx(20.0)

    # B_9: greutatea = 2.0 (exact pe limita penalizarii de 2kg)
    def test_boundary_weight_on_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 2, 'is_fragile': False}]) == pytest.approx(20.0)

    # B_10: greutatea = 2.01 (imediat peste limita penalizarii de 2kg)
    def test_boundary_weight_above_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 2.01, 'is_fragile': False}]) == pytest.approx(20.02)

    # B_11: distanta = 1000 (limita maxima valida)
    def test_max_boundary_distance(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1000, 'weight': 2, 'is_fragile': False}])==pytest.approx(1010.0)

    # B_12: distanta = 1000.01 (imediat peste limita maxima - invalid)
    def test_above_max_boundary_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 1000.01, 'weight': 2, 'is_fragile': False}])

    # B_13: greutatea = 200 (limita maxima valida)
    def test_max_boundary_weight(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 200, 'is_fragile': False}])==pytest.approx(416.0)

    # B_14: greutatea = 200.01 (imediat peste limita maxima - invalid)
    def test_above_max_boundary_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 200.01, 'is_fragile': False}])

    # B_15: cel mai scump/extrem colet posibil (distanta max, greutate max, fragil)
    def test_boundary_max_weight_distance_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1000, 'weight': 200, 'is_fragile': True}])==pytest.approx(2109.0)

    # B_16: frontiera maxima inainte de a iesi din costul fix
    def test_boundary_fixed_cost_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 4.99, 'weight': 4.99, 'is_fragile': True}])==pytest.approx(22.5)

    # B_17: frontiera lista: numar de pachete > 1
    def test_boundary_two_packages_total(self):
        packages = [
            {'distance': 2,  'weight': 2, 'is_fragile': False},
            {'distance': 10, 'weight': 5, 'is_fragile': False},
        ]
        assert ShippingCostCalculator.calculate_cost(packages)==pytest.approx(41.0)

    # B_18: frontiera lista: pachet invalid fix la finalul listei
    def test_boundary_invalid_last_package(self):
        packages = [
            {'distance': 10, 'weight': 5,   'is_fragile': False},
            {'distance': 10, 'weight': 201, 'is_fragile': False},
        ]
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(packages)

    #- # test pentru mutanti
    def test_boundary_weight_bigger(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 10, 'is_fragile': False}])==pytest.approx(28.0)


