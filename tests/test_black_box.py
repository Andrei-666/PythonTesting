import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
Teste black box (partitionare de echivalenta si analiza valorilor de frontiera)

1.Clase de echivanenta:
Parametri:
    distanta
        d1- distanta<=0 (invalida jos)
        d2- 0<distanta<=1000km (valida)
        d3- distanta>1000 (invalida sus)
    
    greutatea
        w1- greutatea<=0 (invalida jos)
        w2- 0<greutatea<=200 (valida)
        w3- greutatea>200 (invalida sus)
    
    fragil
        f1- false
        f2- true

Iesiri:
    1- tarif fix daca distanta<5 si greutatea<5 (base=15.0)
    2- formula standard (10+distanta+max(0,2*(greutatea-2)))


2.Valori de frontiera
distanta: 0(invalid), 0.01(minim valid), 4.99(sub limita de base cost), 5.0(pe limita de la formula), 1000(maxim valid), 1000.01 (invalid)
greutatea: 0(invalid), 0.1(minim valid), 2.0(pe limita de la formula), 4.99(sub limita de base cost), 5.0(pe limita de base cost), 200(maxim valid), 200.01(invalid)


"""




"""equivalence partitioning"""

#distanta <0
def test_equivalence_partitioning_negative_distance():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(-10,5,False)

#distanta = 0
def test_equivalence_partitioning_zero_distance():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(0,5,False)

#greutatea <0 
def test_equivalence_partitioning_negative_weight():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(10,-1,False)

#greutatea=0
def test_equivalence_partitioning_zero_weight():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(10,0,False)  

#distanta>1000 (limita)
def test_equivalence_partitioning_distance_above_limit():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(1500,1,False)

#greutatea>200 (limita)
def test_equivalence_partitioning_weight_above_limit():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(10,250,False)






"""fixed cost-basic package"""

#costul fix (greutate si distanta mici); nefragil
def test_equivalence_partitioning_fixed_cost_non_fragile():
    assert ShippingCostCalculator.calculate_cost(2,2,False)==pytest.approx(15.0)

#costul fix (greutate si distanta mici); fragil
def test_equivalence_partitioning_fixed_cost_fragile():
    assert ShippingCostCalculator.calculate_cost(2,2,True)==pytest.approx(22.5)





"""formula"""

#pachet normal, nefragil = 10+10+max(0,2*(5-2))
def test_equivalence_partitioning_standard_non_fragile():
    assert ShippingCostCalculator.calculate_cost(10,5,False)==pytest.approx(26.0)

#pachet normal fragil = nefragil*1.5
def test_equivalence_partitioning_standard_fragile():
    assert ShippingCostCalculator.calculate_cost(10,5,True)==pytest.approx(39.0)

#colet usor, sub 2kg, fara penalizare pe greutate
def test_equivalence_partitioning_below_penalty_light():
    assert ShippingCostCalculator.calculate_cost(50,1,False)==pytest.approx(60.0)

#colet greu, peste 2kg, cu penalizare pe greutate
def test_equivalence_partitioning_above_penalty_heavy():
    assert ShippingCostCalculator.calculate_cost(100,100,False)==pytest.approx(306.0)






"""boundary limits"""

#distanta=0 invalid
def test_boundary_zero_distance():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(0,5,False)

#distanta=0.01 valid
def test_boundary_minimum_valid_distance():
    assert ShippingCostCalculator.calculate_cost(0.01,1,False) ==pytest.approx( 15.0)

#distanta=0.01, greutatea=5 valid, peste pragul de cost fix
def test_boundary_minimum_valid_formula():
    assert ShippingCostCalculator.calculate_cost(0.01,5,False) == pytest.approx(16.01)




#distanta sub limita de 5 din formula - pret fix 
def test_boundary_distance_below_formula_limit():
    assert ShippingCostCalculator.calculate_cost(4.99,1,False) == pytest.approx(15.0)

#distanta egala cu limita de 5 din formula - pret calculat
def test_boundary_distance_on_formula_limit():
    assert ShippingCostCalculator.calculate_cost(5.0,3,False) == pytest.approx(17.0)

#distanta peste limita de 5 din formula - pret calculat
def test_boundary_distance_above_formula_limit():
    assert ShippingCostCalculator.calculate_cost(5.01,1,False) == pytest.approx(15.01)


#greutatea sub limita de 5 din formula - pret fix 
def test_boundary_weight_below_formula_limit():
    assert ShippingCostCalculator.calculate_cost(1,4.99,False) == pytest.approx(15.0)

#greutatea egala cu limita de 5 din formula - pret calculat
def test_boundary_weight_on_formula_limit():
    assert ShippingCostCalculator.calculate_cost(1,5.0,False) == pytest.approx(17.0)



#penalizare greutate =1.99 (limita 2)
def test_boundary_weight_below_penalty():
    assert ShippingCostCalculator.calculate_cost(10,1.99,False) == pytest.approx(20.0)

#penalizare greutate =2 (limita 2)
def test_boundary_weight_on_penalty():
    assert ShippingCostCalculator.calculate_cost(10,2,False) == pytest.approx(20.0)

#penalizare greutate =2.01 (limita 2)
def test_boundary_weight_above_penalty():
    assert ShippingCostCalculator.calculate_cost(10,2.01,False) == pytest.approx(20.02)





#distanta=1000 (valid)
def test_max_boundary_distance():
    assert ShippingCostCalculator.calculate_cost(1000,2,False)==pytest.approx(1010.0)

#distanta =1000.01(invalid)
def test_above_max_boundary_distance():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(1000.01,2,False)

#greutatea=200 (valid)
def test_max_boundary_weight():
    assert ShippingCostCalculator.calculate_cost(10,200,False)==pytest.approx(416.0)

#distanta =1000.01(invalid)
def test_above_max_boundary_weight():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(10,200.1,False)




#cel mai scump colet posibil
def test_boundary_max_weight_distance_fragile():
    assert ShippingCostCalculator.calculate_cost(1000,200,True)==pytest.approx(2109.0)

#tarif fix plus colet fragil
def test_boundary_fixed_cost_fragile():
    assert ShippingCostCalculator.calculate_cost(4.99,4.99,True)==pytest.approx(22.5)







