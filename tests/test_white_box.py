import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
Teste black box

Graf
noduri

n1-start
n2- if distance<=0 or weight<=0 ===D1
n3-raise VaLueError (valori negative)
n4- if distance>1000 ===D2
n5- raise ValueError (distanta prea mare)
n6-if weight>200 === D3
n7- raise ValueError (greutate prea mare)
n8- if distance<5 and weight<5=== D4
n9- base_cost=15.0
n10- base_cost=10.0+x+y
n11- if is_fragile ===D5
n12=base_count=base_count*1.5
n13- return base_count

branches:
D1=True: N2->N3
D1=False: N2->N4
D2=True: N4->N5
D2=False: N4->N6
D3=True: N6->N7
D3=False: N6->N8
D4=True: N8->N9
D4=False: N8->N10
D5=True: N11->N12
D5=False: N11->N13
"""


#N2->N3 (true) 0<=0 sau 5<=0
def test_statement_coverage_invalid_input():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(0,5,False)

#N4->N5(true) 1001>1000
def test_statement_coverage_distance_over_limit():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(1001,5,False)

#N6->N7(true) 201>200
def test_statement_coverage_weight_over_limit():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost(10,201,False)

#N8->N9 (true) 2<5 and 2<5 => base=15
def test_statement_coverage_fixed_cost():
    assert ShippingCostCalculator.calculate_cost(2,2,False)==pytest.approx(15.0)

#N8->N10 10<5 and 2<5 => cost=10+10+6=26
def test_statement_coverage_basic_formula():
    assert ShippingCostCalculator.calculate_cost(10,5,False)==pytest.approx(26.0)

#N11->N12 (true) is_fragile=True => base=base*1.5
def test_statement_coverage_fragile():
    assert ShippingCostCalculator.calculate_cost(10,5,True)==pytest.approx(39.0)





