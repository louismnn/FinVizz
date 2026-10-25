from math import isclose, isfinite

def check_default(S, sigma, q, r) -> list:

    return [
        (lambda: 0 < S < 250, "The underlying price must be greater than 0 and at most 249"),
        (lambda: sigma > 0, "Volatility must be greater than 0"),
        (lambda: isfinite(sigma), "Volatility must be a finite number"),
        (lambda: 0 <= q <= 1, "Dividend yield must be between 0 and 1"),
        (lambda: -0.1 <= r <= 0.6, "Risk-free rate must be between -0.1 and 0.6"),
        ]

def check_perpetual(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: 1 >= q > 0, "Dividend yield must be greater than 0 for perpetual options"),
        (lambda: 0.6 >= r > 0, "Risk-free rate must be greater than 0 for perpetual options"),
        ] + check_default(S, sigma, q, r)

def check_basic_options(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: T > 0, "Time-to-maturity must be greater than 0"),
        (lambda: T < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
        (lambda: 0 < K < 250, "Strike must be between 0 and 250"),
        ] + check_default(S, sigma, q, r)

def check_spreads_strangles(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: T > 0, "Time-to-maturity must be greater than 0"),
        (lambda: T < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
        (lambda: 0 < K1 < 250, "Strikes must be between 0 and 250"),
        (lambda: 0 < K2 < 250, "Strikes must be between 0 and 250"),
        (lambda: K2 > K1, "Strike two must be greater than strike one"),
        ] + check_default(S, sigma, q, r)

def check_butterfly(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

     return [
        (lambda: T > 0, "Time-to-maturity must be greater than 0"),
        (lambda: T < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
        (lambda: 0 < K1 < 250, "Strikes must be between 0 and 250"),
        (lambda: 0 < K2 < 250, "Strikes must be between 0 and 250"),
        (lambda: 0 < K3 < 250, "Strikes must be between 0 and 250"),
        (lambda: K1 < K2 < K3, "Strikes must have this order: K1 < K2 < K3"),
        (lambda: (K3 - K2) == (K2 - K1), "Strikes must be symetric: K3 - K2 == K2 - K1")
        ] + check_default(S, sigma, q, r)

def check_iron_condor(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: 0 < K1 < K2 < K3 < K4, "Strikes must be greater than 0 and greater than the previous strike"),
        (lambda: isclose((K4 - K3), (K2 - K1)), "Strikes must be symetric: K4 - K3 == K2 - K1"),
        (lambda: T > 0, "Maturity must be greater than 0"),
        (lambda: T < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
    ] + check_default(S, sigma, q, r)

def check_calendar_spreads(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: T2 > T1, "Second time-to-maturity must be greater than the first maturity date"),
        (lambda: T2 < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
        (lambda: T1 > 0, "Times-to-maturity must be greater than 0"),
        (lambda: K2 > K1, "Second strike must be greater than the first strike")
    ] + check_default(S, sigma, q, r)

def check_gap_options(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: 250 > K1 > 0, "Strikes must be between 0 and 250"),
        (lambda: 250 > K2 > 0, "Strikes must be between 0 and 250"),
        (lambda: T > 0, "Time-to-maturity must be greater than 0"),
        (lambda: T < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
    ] + check_default(S, sigma, q, r)

def check_forward_options(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> list:

    return [
        (lambda: T2 > T1 > 0, "Maturities must be greater than 0 and T2 must be greater than T1"),
        (lambda: T2 < 15, "Time-to-maturity is too large, you should select perpetual options instead"),
    ] + check_default(S, sigma, q, r)

def check_errors(product, S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r):

    list_products = {
        "Long Perpetual Call": check_perpetual,
        "Short Perpetual Call": check_perpetual,
        "Long Perpetual Put": check_perpetual,
        "Short Perpetual Put": check_perpetual,
        'Long Call Option': check_basic_options,
        'Long Put Option': check_basic_options,
        'Short Call Option': check_basic_options,
        'Short Put Option': check_basic_options,
        'Long Straddle': check_basic_options,
        'Short Straddle': check_basic_options,
        'Long Binary Call': check_basic_options,
        'Short Binary Call': check_basic_options,
        'Long Binary Put': check_basic_options,
        'Short Binary Put': check_basic_options,
        'Long Strangle': check_spreads_strangles,
        'Short Strangle': check_spreads_strangles,
        'Long Bear Spread': check_spreads_strangles,
        'Short Bear Spread': check_spreads_strangles,
        'Long Bull Spread': check_spreads_strangles,
        'Short Bull Spread': check_spreads_strangles,
        'Long Butterfly': check_butterfly,
        'Short Butterfly': check_butterfly,
        'Short Iron Butterfly': check_butterfly,
        'Long Iron Butterfly': check_butterfly,
        'Long Iron Condor': check_iron_condor,
        'Short Iron Condor': check_iron_condor,
        'Long Calendar Call Spread': check_calendar_spreads,
        'Short Calendar Call Spread': check_calendar_spreads,
        'Long Calendar Put Spread': check_calendar_spreads,
        'Short Calendar Put Spread': check_calendar_spreads,
        "Long Gap Call": check_gap_options,
        "Long Gap Put": check_gap_options,
        "Short Gap Call": check_gap_options,
        "Short Gap Put": check_gap_options,
        "Long Forward Call": check_forward_options,
        "Short Forward Call": check_forward_options,
        "Long Forward Put": check_forward_options,
        "Short Forward Put": check_forward_options,
    }

    function = list_products.get(product, ValueError(f"Product not in the list: {product}"))

    for is_valid, message in function(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r):
        if not is_valid():
            raise ValueError(message)
