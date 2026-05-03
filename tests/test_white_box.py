import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
Teste black box

Graf
noduri

n1-start
n2- if len(packages)==0                 === D1
n3- raise ValueError (lista goala)
n4- total_cost = 0.0
n5- for pkg in packages                 === D2 (loop)
n6- distance, weight, is_fragile = pkg[...]
n7- if distance<=0 or weight<=0         === D3
n8-raise VaLueError (valori negative)
n9- if distance>1000                    === D4
n10- raise ValueError (distanta prea mare)
n11-if weight>200                        === D5
n12- raise ValueError (greutate prea mare)
n13- if distance<5 and weight<5         === D6
n14- base_cost=15.0
n15- base_cost=10.0+x+y
n16- if is_fragile                      === D7
n17=base_count=base_count*1.5
n18- total_cost=total_cost+base_cost
n19- return base_count

branches:
D1=True: N2->N3
D1=False: N2->N4->N5
D2=True(mai sunt pachete): N5->N6->N7
D2=False(loop terminat): N5->N19
D3=True: N7->N8
D3=False: N7->N9
D4=True: N9->N10
D4=False: N9->N11
D5=True: N11->N12
D5=False: N11->N13
D6=True: N13->N14->N18
D6=False: N13->N15->N18
D7=True: N16->N17->N18
D7=False: N16->N18


conditions:
D3: distance<=0 or weight<=0
    c1a distance<=0
    c1b weight<=0

D6: distance<5 and weight<5
    C4a distance<5
    C4b weight<5

D7: is_fragile=True
    C5a is_fragile=True

Circuite
n=19 noduri
e=22 muchii
e-n+2=5 circuite independente

    

"""

#helper
def pkg(distance, weight, is_fragile):
    return [{'distance': distance, 'weight': weight, 'is_fragile': is_fragile}]


"""    Statement coverage    ---------------------------------------------------------------------------




 """
class TestStatementCoverage:
    def test_statement_empty_list(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #N2->N3 (true) 0<=0 sau 5<=0
    def test_statement_coverage_invalid_input(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))

    #N4->N5(true) 1001>1000
    def test_statement_coverage_distance_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))

    #N6->N7(true) 201>200
    def test_statement_coverage_weight_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,201,False))

    #N8->N9 (true) 2<5 and 2<5 => base=15
    def test_statement_coverage_fixed_cost(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #N8->N10 10>=5 and 2<5 => cost=10+10+6=26
    def test_statement_coverage_basic_formula(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #N11->N12 (true) is_fragile=True => base=base*1.5
    def test_statement_coverage_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)





class TestDecisionCoverage:
    """-------------------------------------------------------------------------------------------------------
    D1: distance<=0 or weight<=0  
    D2: distance > 1000 
    D3: weight > 200 
    D4: distance<5 and weight<5 
    D5: is_fragile = True


    """


    def test_decision_d1_true_empty(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    
    def test_decision_coverage_d1_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #D3 true: distance <=0 sau weight<=0
    def test_decision_coverage_d3_true_invalid_negative(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(-1, 5, False))
    #D3 false: distance>0 siweight>0    
    def test_decision_coverage_d3_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)


    #D4 true: distance>1000
    def test_decision_coverage_d4_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))
    #D4 false: distance<=1000
    def test_decision_coverage_d4_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)



    #D5 true: weight>200
    def test_decision_coverage_d3_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,201,False))
    #D5 false: weight<=200
    def test_decision_coverage_d3_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #D6 true: distance<5 si weight<5
    def test_decision_coverage_d4_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #D6 false distance>=5 sau weight>=5
    def test_decision_coverage_d4_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(5,3,False))==pytest.approx(17.0)

    #D7 true: is_fragile=True
    def test_decision_coverage_d5_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)

    #D7 false: is_fragile=False
    def test_decision_coverage_d5_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)






class TestConditionCoverage:
    """------------------------------------------------------------------------------------------------
    conditions:
    D1: distance<=0 or weight<=0
        c1a distance<=0
        c1b weight<=0

    D4: distance<5 and weight<5
        C4a distance<5
        C4b weight<5

    D5: is_fragile = True
        C5a is_fragile=True


    """
    #c1a distance<=0
    def test_condition_coverage_c1a_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))

    def test_condition_coverage_c1a_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)   


    #c1b weight<=0
    def test_condition_coverage_c1b_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,0,False))

    def test_condition_coverage_c1b_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #c4a distance<5
    def test_condition_coverage_c4a_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    def test_condition_coverage_c4a_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,2,False))==pytest.approx(20.0)


    #c4b weight<5
    def test_condition_coverage_c4b_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    def test_condition_coverage_c4b_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(1,5,False))==pytest.approx(17.0)

    #c5a is_fragile=True
    def test_condition_coverage_c5a_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)

    def test_condition_coverage_c5a_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)




class TestIndependentPaths:
    """circuite independente ------------------------------------------------------------------------------
    5 circuite independente
    
    C1:N1->N2(True)->N3 (lista goala)
    
    C2: N1->N2(False)->N4->N5(False)->N19 (lista nevida dar loop ul nu ruleaza)

    C3: N1->N2(False)->N4->N5(True)->N6->N7(True)->N8 (date invalide)

    C4: N1->N2(False)->N4->N5(True)->N6->N7(False)->N9(False)->N11(False)->N13(True)->N14->N16(False)->N18->N5(False)->N19 (fragil, formula, un pachet)
    
    C5:N1->N2(False)->N4->N5(True)->N6->N7(False)->N9(False)->N11(False)->N13(False)->N15->N16(True)->N17->N18->N5(True)->...........->N5(false)->N19 (fragil, formula, pachete multiple)
    """

    def test_circuit_1_empty_list(self):
        #C1: N1->N2(T)->N3
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])
 
    def test_circuit_2_invalid_package(self):
        #C3: N5(T)->N6->N7(T)->N8
        #pachet cu distance negativa=>raise in prima iteratie
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))
 
    def test_circuit_3_distance_over_limit(self):
        #N9(T)->N10: distance>1000=>raise
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))
 
    def test_circuit_4_flat_rate_non_fragile(self):
        #C4:toate validarile trec, cost fix, nefragil, un pachet
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)
 
    def test_circuit_5_formula_fragile_multiple(self):
        #C5: formula, fragil, loop de 2 ori
        #pachet1:15.0, pachet2:39.0 =>total=54.0
        packages = [
            {'distance': 2,  'weight': 2, 'is_fragile': False},
            {'distance': 10, 'weight': 5, 'is_fragile': True},
        ]
        assert ShippingCostCalculator.calculate_cost(packages) == pytest.approx(54.0)



