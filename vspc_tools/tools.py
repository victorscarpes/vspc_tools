from to_precision import eng_notation as _eng_
from to_precision import sci_notation as _sci_

def eng_notation(value:float, unit:str, precision:int, decimal:str=',') -> str:
    string = _eng_(value, precision, 'E')
    string = string.replace('.E', 'E').replace('.', decimal)
    exps = ['E24', 'E21', 'E18', 'E15', 'E12', 'E9', 'E6', 'E3', 'E0', 'E-3', 'E-6', 'E-9', 'E-12', 'E-15', 'E-18', 'E-21', 'E-24']
    prefs = ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', '', 'm', 'μ', 'n', 'p', 'f', 'a', 'z', 'y']
    for (exp, pref) in zip(exps, prefs):
        string = string.replace(exp, ' '+pref)
    return string + unit

def sci_notation(value:float, unit:str, precision:int, decimal:str=',') -> str:
    string = _sci_(value, precision, 'E')
    string = string.replace('.E', 'E').replace('.', decimal)
    mantissa, exponent = string.split('E')
    simbs = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    supers = ['⁻', '⁰', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    if exponent == '0':
        return mantissa + unit
    else:
        for (simb, super) in zip(simbs, supers):
            exponent = exponent.replace(simb, super)
    return mantissa + ' × 10' + exponent + ' ' + unit

def eng_formatter(unit:str, precision:int, decimal:str=',') -> callable:
    def func(x, pos=None):
        return eng_notation(x, unit, precision, decimal)
    return func

def sci_formatter(unit:str, precision:int, decimal:str=',') -> callable:
    def func(x, pos=None):
        return sci_notation(x, unit, precision, decimal)
    return func