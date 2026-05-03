import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


"""
Teste black box (partitionare de echivalenta si analiza valorilor de frontiera)

1.Clase de echivanenta:
Parametri:
    packages
        l1-lista goala(invalida)
        l2-lista cu un pachet valid
        l3-lista cu mai multe pachete valide
        l4-lista cu un pachet invalid in interior


    distanta
        d1- distanta<=0 (invalida jos)
        d2- 0<distanta<5(valida, zona cost fix)
        d3- 5<=distanta<=1000km (valida, zona formula)
        d4- distanta>1000 (invalida sus)
    
    greutatea
        w1- greutatea<=0 (invalida jos)
        w2- 0<greutatea<2 (valida, fara penalizare)
        w3- 2<=greutatea<5(valida, cost fix)
        w4- 0<greutatea<=200 (valida, cu penalizare)
        w5- greutatea>200 (invalida sus)
    
    fragil
        f1- false
        f2- true

Iesiri:
    1- tarif fix daca distanta<5 si greutatea<5 (base=15.0)
    2- formula standard (10+distanta+max(0,2*(greutatea-2)))


2.Valori de frontiera
distanta: 0(invalid), 0.01(minim valid), 4.99(sub limita de base cost), 5.0(pe limita de la formula), 1000(maxim valid), 1000.01 (invalid)
greutatea: 0(invalid), 0.01(minim valid), 2.0(pe limita de la formula), 4.99(sub limita de base cost), 5.0(pe limita de base cost), 200(maxim valid), 200.01(invalid)


"""



class TestEquivalencePartitioning:  
    """equivalence partitioning"""

    #invalid list --------------------------------------------

    def test_equivalence_partitioning_empty_packages(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([])

    #invalid distance ------------------------------------------------

    #distanta <0
    def test_equivalence_partitioning_negative_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': -10, 'weight': 5, 'is_fragile': False}])

    #distanta = 0
    def test_equivalence_partitioning_zero_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 0, 'weight': 5, 'is_fragile': False}])

    #distanta>1000 (limita)
    def test_equivalence_partitioning_distance_above_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 1500, 'weight': 5, 'is_fragile': False}])


    #invalid weight---------------------------------------------------

    #greutatea <0 
    def test_equivalence_partitioning_negative_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': -1, 'is_fragile': False}])

    #greutatea=0
    def test_equivalence_partitioning_zero_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 0, 'is_fragile': False}])

    #greutatea>200 (limita)
    def test_equivalence_partitioning_weight_above_limit(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 250, 'is_fragile': False}])




    #fixed cost -------------------------------------------------------------

    """fixed cost-basic package"""

    #costul fix (greutate si distanta mici); nefragil
    def test_equivalence_partitioning_fixed_cost_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 2, 'is_fragile': False}])==pytest.approx(15.0)

    #costul fix (greutate si distanta mici); fragil
    def test_equivalence_partitioning_fixed_cost_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 2, 'is_fragile': True}])==pytest.approx(22.5)



    #standard formula ---------------------------------------------------------------------

    """formula"""

    #pachet normal, nefragil = 10+10+max(0,2*(5-2))
    def test_equivalence_partitioning_standard_non_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 5, 'is_fragile': False}])==pytest.approx(26.0)

    #pachet normal fragil = nefragil*1.5
    def test_equivalence_partitioning_standard_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 5, 'is_fragile': True}])==pytest.approx(39.0)

    #colet usor, sub 2kg, fara penalizare pe greutate
    def test_equivalence_partitioning_below_penalty_light(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 50, 'weight': 1, 'is_fragile': False}])==pytest.approx(60.0)

    #colet greu, peste 2kg, cu penalizare pe greutate
    def test_equivalence_partitioning_above_penalty_heavy(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 100, 'weight': 100, 'is_fragile': False}])==pytest.approx(306.0)


    #multiple packages -----------------------------------------------------
    def test_equivalence_partitioning_multiple_packages(self):
        #fixed cost+formula+fragile=15+26+39=80
        packages = [
                {'distance': 2,  'weight': 2, 'is_fragile': False},
                {'distance': 10, 'weight': 5, 'is_fragile': False},
                {'distance': 10, 'weight': 5, 'is_fragile': True},
            ]
        assert ShippingCostCalculator.calculate_cost(packages)==pytest.approx(80.0)

    def test_equivalence_partitioning_invalid_package_in_middle(self):

        packages = [
            {'distance': 10, 'weight': 5,   'is_fragile': False},
            {'distance': -1, 'weight': 5,   'is_fragile': False},
            {'distance': 10, 'weight': 5,   'is_fragile': False},
        ]
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(packages)


class TestBoundaryValueAnalysis:
    """boundary limits"""

    #distanta=0 invalid
    def test_boundary_zero_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 0, 'weight': 5, 'is_fragile': False}])

    # distanta=0.01, greutatea=5 valid, peste pragul de cost fix
    def test_boundary_minimum_valid_formula(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 0.01, 'weight': 5, 'is_fragile': False}]) == pytest.approx(16.01)




    # distanta sub limita de 5 din formula - pret fix 
    def test_boundary_distance_below_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 4.99, 'weight': 1, 'is_fragile': False}]) == pytest.approx(15.0)

    #distanta egala cu limita de 5 din formula - pret calculat
    def test_boundary_distance_on_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 5.0, 'weight': 3, 'is_fragile': False}]) == pytest.approx(17.0)

    #distanta peste limita de 5 din formula - pret calculat
    def test_boundary_distance_above_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 5.01, 'weight': 1, 'is_fragile': False}]) == pytest.approx(15.01)


    #greutatea sub limita de 5 din formula - pret fix 
    def test_boundary_weight_below_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1, 'weight': 4.99, 'is_fragile': False}])==pytest.approx(15.0)

    #greutatea egala cu limita de 5 din formula - pret calculat
    def test_boundary_weight_on_formula_limit(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1, 'weight': 5.0, 'is_fragile': False}]) == pytest.approx(17.0)



    #penalizare greutate =1.99 (limita 2)
    def test_boundary_weight_below_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 1.99, 'is_fragile': False}]) == pytest.approx(20.0)

    #penalizare greutate =2 (limita 2)
    def test_boundary_weight_on_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 2, 'is_fragile': False}]) == pytest.approx(20.0)

    #penalizare greutate =2.01 (limita 2)
    def test_boundary_weight_above_penalty(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 2.01, 'is_fragile': False}]) == pytest.approx(20.02)





    #distanta=1000 (valid)
    def test_max_boundary_distance(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1000, 'weight': 2, 'is_fragile': False}])==pytest.approx(1010.0)

    #distanta =1000.01(invalid)
    def test_above_max_boundary_distance(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 1000.01, 'weight': 2, 'is_fragile': False}])

    #greutatea=200 (valid)
    def test_max_boundary_weight(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 200, 'is_fragile': False}])==pytest.approx(416.0)

    #distanta =1000.01(invalid)
    def test_above_max_boundary_weight(self):
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost([{'distance': 10, 'weight': 200.01, 'is_fragile': False}])




    #cel mai scump colet posibil
    def test_boundary_max_weight_distance_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 1000, 'weight': 200, 'is_fragile': True}])==pytest.approx(2109.0)

    #tarif fix plus colet fragil
    def test_boundary_fixed_cost_fragile(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 4.99, 'weight': 4.99, 'is_fragile': True}])==pytest.approx(22.5)


    def test_boundary_two_packages_total(self):
        packages = [
            {'distance': 2,  'weight': 2, 'is_fragile': False},
            {'distance': 10, 'weight': 5, 'is_fragile': False},
        ]
        assert ShippingCostCalculator.calculate_cost(packages)==pytest.approx(41.0)

    def test_boundary_invalid_last_package(self):
        packages = [
            {'distance': 10, 'weight': 5,   'is_fragile': False},
            {'distance': 10, 'weight': 201, 'is_fragile': False},
        ]
        with pytest.raises(ValueError):
            ShippingCostCalculator.calculate_cost(packages)

    def test_boundary_weight_bigger(self):
        assert ShippingCostCalculator.calculate_cost([{'distance': 2, 'weight': 10, 'is_fragile': False}])==pytest.approx(28.0)




