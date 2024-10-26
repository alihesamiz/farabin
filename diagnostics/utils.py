from django.utils.translation import gettext_lazy as _
from math import log2

def get_life_cycle(financial_assets):
    # Initialize x_vals and y_vals for graphical representation
    x_vals = [_("Start"), _("Introduction"), _("Growth"), _("Maturity"),
              _("Recession 1"), _("Recession 2"), _("Recession 3"),
              _("Decline 1"), _("Decline 2")]
    x_vals_numerical = [1, 1.5, 2, 2.5, 4, 4.5, 4, 3, 2]
    y_vals = [log2(x) for x in x_vals_numerical]

    # Get the last financial asset
    finance = financial_assets.last()
    if not finance:
        return 5, x_vals, y_vals

    # Retrieve life cycles based on capital_providing values
    life_cycles = finance.capital_providing_method.values_list('capital_providing', flat=True)

    # Define mappings for capital_providing combinations
    cycle_mappings = {
        ('operational', 'finance'): 7,
        ('operational', 'invest'): 6,
        ('finance', 'invest'): 2,
        ('operational',): 8,
        ('finance',): 1,
        ('invest',): 3
    }

    # Sort and tuple the life cycle values for lookup
    sorted_cycles = tuple(sorted(life_cycles))
    life_cycle = cycle_mappings.get(sorted_cycles, 5) if len(sorted_cycles) <= 2 else 5

    return life_cycle, x_vals, y_vals
