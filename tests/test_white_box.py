import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
Teste white box

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
n15-base_cost=10.0+distance+max(0,2.0*(weight-2))
n16- if is_fragile                      === D7
n17=base_cost=base_cost*fragile_multiplier
n18- total_cost=total_cost+base_cost
n19- return total_cost
Exit(20)

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

D6=True: N13->N14->N16
D6=False: N13->N15->N16

D7=True: N16->N17->N18
D7=False: N16->N18


conditions:
D1:
    c1=len(packages)==0

D2:
    c2=mai exista pachete de procesat    

D3:
    c3a=distance<=0
    c3b=weight<=0

D4:
    c4=distance>1000

D5:
    c5=weight>200

D6:
    c6a=distance<5
    c6b=weight<5

D7:
    c7=is_fragile

    

Circuite:

Pentru graful de flux de control:
n=20 noduri
e=26 muchii
e-n+2=26-20+2=8 circuite independente

    

"""

#helper
def pkg(distance, weight, is_fragile):
    return [{'distance': distance, 'weight': weight, 'is_fragile': is_fragile}]


"""    Statement coverage    ---------------------------------------------------------------------------

pentru acoperire la nivel de instructiune, alegem date de test astfel incat fiecare nod relevant din graf sa fie parcurs cel putin o data

Intrari                         Rezultat(expected)       Instructiuni parcurse

[]                              ValueError               N1,N2,N3,Exit

[(0,5,F)]                       ValueError               N1,N2,N4,N5,N6,N7,N8,Exit

[(1001,5,F)]                    ValueError               N1,N2,N4,N5,N6,N7,N9,N10,Exit

[(10,201,F)]                    ValueError               N1,N2,N4,N5,N6,N7,N9,N11,N12,Exit

[(2,2,F)]                       15.0                     N1,N2,N4,N5,N6,N7,N9,N11,N13,N14,N16,N18,N5,N19,Exit

[(10,5,F)]                      26.0                     N1,N2,N4,N5,N6,N7,N9,N11,N13,N15,N16,N18,N5,N19,Exit

[(10,5,T)]                      39.0                     N1,N2,N4,N5,N6,N7,N9,N11,N13,N15,N16,N17,N18,N5,N19,Exit


 """
class TestStatementCoverage:
    #s_1: ([]), N1,N2,N3,Exit
    def test_statement_empty_list(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #s_2: ([(0,5,F)]), N7->N8
    def test_statement_coverage_invalid_input(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))

    #s_3: ([(1001,5,F)]), N9->N10
    def test_statement_coverage_distance_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))

    #s_4: ([(10,201,F)]), N11->N12
    def test_statement_coverage_weight_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,201,False))

     #s_5: ([(2,2,F)]), N13->N14
    def test_statement_coverage_fixed_cost(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #s_6: ([(10,5,F)]), N13->N15
    def test_statement_coverage_basic_formula(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #s_7: ([(10,5,T)]), N16->N17
    def test_statement_coverage_fragile(self):
         assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)





class TestDecisionCoverage:
    """-------------------------------------------------------------------------------------------------------

    pentru acoperire la nivel de decizie, fiecare decizie trebuie sa ia atat valoarea true, cat si valoarea false

Decizii
    D1: if len(packages)==0
    D2: for pkg in packages
    D3: distance<=0 or weight<=0  
    D4: distance > 1000 
    D5: weight > 200 
    D6: distance<5 and weight<5 
    D7: is_fragile = True

    Intrari                         Rezultat(expected)       Decizii acoperite

    []                              ValueError               D1=True
    [(10,5,F)]                      26.0                     D1=False
    [(10,5,F)]                      26.0                     D2=True, D2=False
    [(-1,5,F)]                      ValueError               D3=True
    [(10,5,F)]                      26.0                     D3=False
    [(1001,5,F)]                    ValueError               D4=True
    [(10,5,F)]                      26.0                     D4=False
    [(10,201,F)]                    ValueError               D5=True
    [(10,5,F)]                      26.0                     D5=False
    [(2,2,F)]                       15.0                     D6=True
    [(5,3,F)]                       17.0                     D6=False
    [(10,5,T)]                      39.0                     D7=True
    [(10,5,F)]                      26.0                     D7=False
    

    """

    #d_1: ([]), D1=True
    def test_decision_d1_true_empty(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #d_2: ([(10,5,F)]), D1=False
    def test_decision_d1_false_non_empty(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #d_3: ([(10,5,F)]), D2=True si D2=False
    #bucla for intra pentru pachetul existent, apoi iese dupa procesarea lui
    def test_decision_d2_true_and_false_loop(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #d_4: ([(-1,5,F)]), D3=True
    def test_decision_d3_true_invalid_negative(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(-1,5,False))

    #d_5: ([(10,5,F)]), D3=False
    def test_decision_d3_false_valid_values(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #d_6: ([(1001,5,F)]), D4=True
    def test_decision_d4_true_distance_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))

    #d_7: ([(10,5,F)]), D4=False
    def test_decision_d4_false_distance_valid(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #d_8: ([(10,201,F)]), D5=True
    def test_decision_d5_true_weight_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,201,False))

    #d_9: ([(10,5,F)]), D5=False
    def test_decision_d5_false_weight_valid(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #d_10: ([(2,2,F)]), D6=True
    def test_decision_d6_true_fixed_cost(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #d_11: ([(5,3,F)]), D6=False
    def test_decision_d6_false_formula_cost(self):
        assert ShippingCostCalculator.calculate_cost(pkg(5,3,False))==pytest.approx(17.0)

    #d_12: ([(10,5,T)]), D7=True
    def test_decision_d7_true_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)

    #d_13: ([(10,5,F)]), D7=False
    def test_decision_d7_false_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)






class TestConditionCoverage:
    """------------------------------------------------------------------------------------------------
D3: distance<=0 or weight<=0
    c3a: distance<=0
    c3b: weight<=0

D6: distance<5 and weight<5
    c6a: distance<5
    c6b: weight<5

D7: is_fragile
    c7: is_fragile

    Intrari                         Rezultat(expected)       Conditii individuale acoperite

    [(0,5,F)]                       ValueError               c3a=True
    [(10,5,F)]                      26.0                     c3a=False
    [(10,0,F)]                      ValueError               c3b=True
    [(10,5,F)]                      26.0                     c3b=False
    [(2,2,F)]                       15.0                     c6a=True
    [(10,2,F)]                      20.0                     c6a=False
    [(2,2,F)]                       15.0                     c6b=True
    [(1,5,F)]                       17.0                     c6b=False
    [(10,5,T)]                      39.0                     c7=True
    [(10,5,F)]                      26.0                     c7=False




    """
    #cc_1: ([(0,5,F)]), c3a=True
    def test_condition_c3a_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))

    #cc_2: ([(10,5,F)]), c3a=False
    def test_condition_c3a_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #cc_3: ([(10,0,F)]), c3b=True
    def test_condition_c3b_true(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,0,False))

    #cc_4: ([(10,5,F)]), c3b=False
    def test_condition_c3b_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #cc_5: ([(2,2,F)]), c6a=True
    def test_condition_c6a_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #cc_6: ([(10,2,F)]), c6a=False
    def test_condition_c6a_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,2,False))==pytest.approx(20.0)

    #cc_7: ([(2,2,F)]), c6b=True
    def test_condition_c6b_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #cc_8: ([(1,5,F)]), c6b=False
    def test_condition_c6b_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(1,5,False))==pytest.approx(17.0)

    #cc_9: ([(10,5,T)]), c7=True
    def test_condition_c7_true(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)

    #cc_10: ([(10,5,F)]), c7=False
    def test_condition_c7_false(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)




class TestIndependentPaths:
    """circuite independente ------------------------------------------------------------------------------
-pentru graful actual:
    n=20
    e=26

    V(G)=26-20+2=8

Rezulta 8 circuite independente

    C1: N1,N2,N3,Exit,N1
        lista goala

    C2: N1,N2,N4,N5,N6,N7,N8,Exit,N1 - pachet invalid prin distance<=0 sau weight<=0

    C3: N1,N2,N4,N5,N6,N7,N9,N10,Exit,N1 - distanta mai mare de 1000

    C4: N1,N2,N4,N5,N6,N7,N9,N11,N12,Exit,N1 - greutate mai mare de 200

    C5: N1,N2,N4,N5,N6,N7,N9,N11,N13,N14,N16,N18,N5,N19,Exit,N1 - cost fix, nefragil, un singur pachet

    C6: N1,N2,N4,N5,N6,N7,N9,N11,N13,N15,N16,N18,N5,N19,Exit,N1 - formula standard, nefragil, un singur pachet

    C7: N1,N2,N4,N5,N6,N7,N9,N11,N13,N15,N16,N17,N18,N5,N19,Exit,N1 - formula standard, fragil, un singur pachet

    C8: N5,N6,N7,N9,N11,N13,N14,N16,N18,N5 - circuitul buclei for, parcurs prin procesarea a cel putin doua pachete

    
    C1: []
    C2: [(0,5,F)]
    C3: [(1001,5,F)]
    C4: [(10,201,F)]
    C5: [(2,2,F)]
    C6: [(10,5,F)]
    C7: [(10,5,T)]
    C8: [(2,2,F),(10,5,T)]


    """

    #C1: N1,N2,N3,Exit,N1
    def test_circuit_1_empty_list(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #C2: N1,N2,N4,N5,N6,N7,N8,Exit,N1
    def test_circuit_2_invalid_distance_or_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(0,5,False))

    #C3: N1,N2,N4,N5,N6,N7,N9,N10,Exit,N1
    def test_circuit_3_distance_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(1001,5,False))

    #C4: N1,N2,N4,N5,N6,N7,N9,N11,N12,Exit,N1
    def test_circuit_4_weight_over_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(pkg(10,201,False))

    #C5: cost fix, nefragil
    def test_circuit_5_fixed_cost_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(2,2,False))==pytest.approx(15.0)

    #C6: formula standard, nefragil
    def test_circuit_6_formula_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,False))==pytest.approx(26.0)

    #C7: formula standard, fragil
    def test_circuit_7_formula_fragile(self):
        assert ShippingCostCalculator.calculate_cost(pkg(10,5,True))==pytest.approx(39.0)

    #C8: circuitul buclei for este parcurs prin doua pachete
    def test_circuit_8_loop_multiple_packages(self):
        packages = [
            {'distance': 2, 'weight': 2, 'is_fragile': False},
            {'distance': 10, 'weight': 5, 'is_fragile': True},
        ]
        assert ShippingCostCalculator.calculate_cost(packages)==pytest.approx(54.0)



