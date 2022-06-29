from to_precision import eng_notation as _eng_
from to_precision import sci_notation as _sci_

"""
Autor: Victor Sabiá Pereira Carpes
Dsecrição: Módulo com funções que eu utilizo o tempo inteiro.
"""

def eng_notation(value:float, unit:str, precision:int, decimal:str=',') -> str:
    """
    Formata um valor numperico utilizando os prefixos do SI para as potências de 10, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        value: Valor a ser formatado.
        unit: Unidade a ser utilizada.
        precision: Quantidade de algarismos significativos.
        decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
    
    Retorno:
        String formatada.
    
    Exemplos:
        >>> eng_notation(0.356, 'm', 3)
        '356 mm'
        >>> eng_notation(0.356, 'V', 2)
        '360 mV'
        >>> eng_notation(1200, 'Hz', 6, '.')
        '1.20000 kHz'
    """

    string = _eng_(value, precision, 'E')
    string = string.replace('.E', 'E').replace('.', decimal)
    exps = ['E24', 'E21', 'E18', 'E15', 'E12', 'E9', 'E6', 'E3', 'E0', 'E-3', 'E-6', 'E-9', 'E-12', 'E-15', 'E-18', 'E-21', 'E-24']
    prefs = ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', '', 'm', 'μ', 'n', 'p', 'f', 'a', 'z', 'y']
    for (exp, pref) in zip(exps, prefs):
        string = string.replace(exp, ' '+pref)
    return string + unit

def sci_notation(value:float, unit:str, precision:int, decimal:str=',') -> str:
    """
    Formata um valor numperico utilizando em notação científica, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        value: Valor a ser formatado.
        unit: Unidade a ser utilizada.
        precision: Quantidade de algarismos significativos.
        decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
    
    Retorno:
        String formatada.

    Exemplos:
        >>> sci_notation(0.356, 'm', 3)
        '3,56 × 10⁻¹ m'
        >>> sci_notation(0.035, 'V', 2)
        '3,5 × 10⁻² V'
        >>> sci_notation(1200, 'Hz', 6, '.')
        '1.20000 × 10³ Hz'
    """

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
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função eng_notation.

    Argumentos:
        unit: Unidade a ser utilizada.
        precision: Quantidade de algarismos significativos.
    
    Retorno:
        Função de formatação.
    
    Exemplos:
        >>> ax.xaxis.set_major_formatter(eng_formatter('V', 3))
    """

    def func(x, pos=None):
        return eng_notation(x, unit, precision, decimal)
    return func

def sci_formatter(unit:str, precision:int, decimal:str=',') -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função sci_notation.

    Argumentos:
        unit: Unidade a ser utilizada.
        precision: Quantidade de algarismos significativos.
    
    Retorno:
        Função de formatação.
    
    Exemplos:
        >>> ax.xaxis.set_major_formatter(sci_formatter('V', 3))
    """

    def func(x, pos=None):
        return sci_notation(x, unit, precision, decimal)
    return func