import pytest
from src.shipping_cost_calculator import ShippingCostCalculator


def test_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost([])


@pytest.mark.parametrize(
    "package",
    [
        {"distance": 0, "weight": 10, "is_fragile": False},
        {"distance": -1, "weight": 10, "is_fragile": False},
        {"distance": 1001, "weight": 10, "is_fragile": False},
    ],
)
def test_invalid_distance_raises_value_error(package):
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost([package])


@pytest.mark.parametrize(
    "package",
    [
        {"distance": 10, "weight": 0, "is_fragile": False},
        {"distance": 10, "weight": -5, "is_fragile": False},
        {"distance": 10, "weight": 201, "is_fragile": False},
    ],
)
def test_invalid_weight_raises_value_error(package):
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost([package])


@pytest.mark.parametrize(
    "package",
    [
        {"distance": 10, "weight": 10, "is_fragile": "yes"},
        {"distance": 10, "weight": 10, "is_fragile": None},
        {"distance": 10, "weight": 10, "is_fragile": 1},
    ],
)
def test_invalid_is_fragile_raises_value_error(package):
    with pytest.raises(ValueError):
        ShippingCostCalculator.calculate_cost([package])


def test_small_distance_and_weight_fixed_cost():
    packages = [
        {"distance": 3, "weight": 4, "is_fragile": False}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    assert result == 15


def test_small_distance_and_weight_fixed_cost_fragile():
    packages = [
        {"distance": 3, "weight": 4, "is_fragile": True}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    assert result == 22.5


def test_standard_formula_without_extra_weight():
    packages = [
        {"distance": 10, "weight": 2, "is_fragile": False}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    # 10 + 10 + max(0, 2*(2-2)) = 20
    assert result == 20


def test_standard_formula_with_extra_weight():
    packages = [
        {"distance": 10, "weight": 5, "is_fragile": False}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    # 10 + 10 + 2*(5-2) = 26
    assert result == 26


def test_standard_formula_fragile():
    packages = [
        {"distance": 10, "weight": 5, "is_fragile": True}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    # (10 + 10 + 6) * 1.5 = 39
    assert result == 39


def test_multiple_packages_total_cost():
    packages = [
        {"distance": 3, "weight": 4, "is_fragile": False},   # 15
        {"distance": 10, "weight": 5, "is_fragile": False},  # 26
        {"distance": 10, "weight": 5, "is_fragile": True},   # 39
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    assert result == 80


def test_boundary_values_are_valid():
    packages = [
        {"distance": 1000, "weight": 200, "is_fragile": False}
    ]

    result = ShippingCostCalculator.calculate_cost(packages)

    expected = 10 + 1000 + 2 * (200 - 2)
    assert result == expected