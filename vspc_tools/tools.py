"""
Autor: Victor Sabiá Pereira Carpes
Descrição: Módulo com funções que eu utilizo o tempo inteiro.
"""

import math as mt

_si_prefix: dict[int, str] = {-30: " q",
                              -27: " r",
                              -24: " y",
                              -21: " z",
                              -18: " a",
                              -15: " f",
                              -12: " p",
                              -9: " n",
                              -6: " μ",
                              -3: " m",
                              0: " ",
                              3: " k",
                              6: " M",
                              9: " G",
                              12: " T",
                              15: " P",
                              18: " E",
                              21: " Z",
                              24: " Y",
                              27: " R",
                              30: " Q"}


def eng_inv(string: str) -> float:
    """
    Converte uma string formatada em notação de engenharia para um valor numérico. 

    Argumentos:
        -string (str): String formatada. A string deve ser formatada utilizando apenas os prefixos do SI correspondentes às potências de 10 com expoente múltiplo de 3. Entre o valor numérico e a unidade é necessário um espaço. O separador decimal pode ser tanto ponto quanto vírgula. O prefixo micro (μ) deve ser digitado como 'u'.

    Retorno:
        -Valor numérico.

    Exemplos:
        >>> eng_inv('356 mm')
        0.356
        >>> eng_inv('360 mV')
        0.36
        >>> eng_inv('1.20000 kHz')
        1200.0
    """

    mantissa, unit = string.split(' ')
    pref_dict = {'Y': 24, 'Z': 21, 'E': 18, 'P': 15, 'T': 12, 'G': 9, 'M': 6, 'k': 3,
                 'm': -3, 'u': -6, 'n': -9, 'p': -12, 'f': -15, 'a': -18, 'z': -21, 'y': -24}
    mantissa = mantissa.replace(',', '.')
    if len(unit) == 1 or unit[0] not in pref_dict:
        exponent = 0
    else:
        exponent = pref_dict[unit[0]]
    return float(mantissa) * 10**exponent


def round_eng(value: int | float, unit: str = '', precision: int = 3, decimal: str = ',') -> str:
    """
    Formata um valor numérico utilizando os prefixos do SI para as potências de 10, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        -value (int | float): Valor a ser formatado.
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        -String formatada.

    Exemplos:
        >>> round_eng(0.356, 'm', 3)
        '356 mm'
        >>> round_eng(0.356, 'V', 2)
        '360 mV'
        >>> round_eng(1200, 'Hz', 6, '.')
        '1.20000 kHz'
    """

    if any(char.isdecimal() for char in decimal):
        decimal = ","

    if precision == 0:
        return ""

    if value < 0:
        return "-"+round_eng(value=abs(value), unit=unit, precision=precision, decimal=decimal)

    if mt.isinf(value):
        if unit == "":
            return "inf"
        else:
            return "inf "+unit

    if mt.isnan(value):
        return "NaN"

    if value == 0:
        long_string = "0"+decimal+(precision-1)*"0"
        if long_string[-1] == decimal:
            long_string = long_string[:-1]
        if unit == "":
            return long_string
        else:
            return long_string + " " + unit

    si_exp = 3*mt.floor(mt.log10(value)/3)
    value_norm = value/(10**si_exp)
    whole, frac = str(value_norm).split(".")
    decimal_point = len(whole)
    long_string = whole + frac

    if len(long_string) == precision:
        return whole + decimal + frac + _si_prefix[si_exp] + unit
    elif len(long_string) < precision:
        long_string += (precision - len(long_string) + 1) * "0"

    long_list = [int(char) for char in long_string]

    digit_before_trunc = long_list[precision-1]
    digit_after_trunc = long_list[precision]

    if digit_after_trunc > 5:
        long_list[precision-1] += 1
    elif digit_after_trunc == 5:
        if set(long_list[precision:]).intersection(set([1, 2, 3, 4, 5, 6, 7, 8, 9])):
            long_list[precision-1] += 1
        elif digit_before_trunc % 2 == 1:
            long_list[precision-1] += 1

    long_list = long_list[:precision]

    index = len(long_list) - 1
    while index > 0:
        current_digit = long_list[index]
        if current_digit > 9:
            long_list[index] -= 10
            long_list[index-1] += 1
        index -= 1

    if long_list[0] > 9:
        decimal_point += 1
        long_list[0] -= 10
        long_list = [1] + long_list

    if decimal_point > 3:
        si_exp += 3
        decimal_point -= 3

    long_string = "".join([str(digit) for digit in long_list])

    n_string = len(long_string)
    if n_string < decimal_point:
        long_string += (decimal_point - n_string) * "0"

    long_string = long_string[:decimal_point] + decimal + long_string[decimal_point:]

    whole, frac = long_string.split(decimal)
    if len(whole) >= precision:
        long_string = whole
    else:
        n_rest = precision - len(whole)
        long_string = whole + decimal + frac[:n_rest]

    return long_string + _si_prefix[si_exp] + unit


def round_sci(value: int | float, unit: str = '', precision: int = 3, decimal: str = ',') -> str:
    """
    Formata um valor numérico em notação científica, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        -value (int | float): Valor a ser formatado.
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        String formatada.

    Exemplos:
        >>> round_sci(0.356, 'm', 3)
        '3,56 × 10⁻¹ m'
        >>> round_sci(0.035, 'V', 2)
        '3,5 × 10⁻² V'
        >>> round_sci(1200, 'Hz', 6, '.')
        '1.20000 × 10³ Hz'
    """

    if any(char.isdecimal() for char in decimal):
        decimal = ","

    if unit != "":
        unit = " "+unit

    if precision == 0:
        return ""

    if value < 0:
        return "-"+round_sci(value=abs(value), unit=unit, precision=precision, decimal=decimal)

    if mt.isinf(value):
        return "inf"+unit

    if mt.isnan(value):
        return "NaN"

    if value == 0:
        long_string = "0"+decimal+(precision-1)*"0"
        if long_string[-1] == decimal:
            long_string = long_string[:-1]
        return long_string + unit

    sci_exp = mt.floor(mt.log10(value))
    value_norm = value/(10**sci_exp)
    whole, frac = str(value_norm).split(".")
    long_string = whole + frac

    if precision == 1:
        decimal = ""

    if len(long_string) == precision:
        if sci_exp == 0:
            return whole + decimal + frac + unit
        elif sci_exp == 1:
            return whole + decimal + frac + " × 10" + unit
        else:
            sci_exp_str = str(sci_exp)
            for digit, symbol in zip(["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["⁻", "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]):
                sci_exp_str = sci_exp_str.replace(digit, symbol)
            return whole + decimal + frac + " × 10" + sci_exp_str + unit
    elif len(long_string) < precision:
        long_string += (precision - len(long_string) + 1) * "0"

    long_list = [int(char) for char in long_string]

    digit_before_trunc = long_list[precision-1]
    digit_after_trunc = long_list[precision]

    if digit_after_trunc > 5:
        long_list[precision-1] += 1
    elif digit_after_trunc == 5:
        if set(long_list[precision:]).intersection(set([1, 2, 3, 4, 5, 6, 7, 8, 9])):
            long_list[precision-1] += 1
        elif digit_before_trunc % 2 == 1:
            long_list[precision-1] += 1

    long_list = long_list[:precision]

    index = len(long_list) - 1
    while index > 0:
        current_digit = long_list[index]
        if current_digit > 9:
            long_list[index] -= 10
            long_list[index-1] += 1
        index -= 1

    if long_list[0] > 9:
        sci_exp += 1
        long_list[0] -= 10
        long_list = [1] + long_list

    long_list = long_list[:precision]

    long_string = "".join([str(digit) for digit in long_list])
    whole = long_string[:1]
    frac = long_string[1:]
    if sci_exp == 0:
        return whole + decimal + frac + unit
    elif sci_exp == 1:
        return whole + decimal + frac + " × 10" + unit
    else:
        sci_exp_str = str(sci_exp)
        for digit, symbol in zip(["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["⁻", "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]):
            sci_exp_str = sci_exp_str.replace(digit, symbol)
        return whole + decimal + frac + " × 10" + sci_exp_str + unit


def round_fix(value: int | float, unit: str = '', precision: int = 3, decimal: str = ',') -> str:
    """
    Formata um valor numérico em notação de ponto fixo, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        -value (int | float): Valor a ser formatado.
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        String formatada.

    Exemplos:
        >>> round_fixed(0.356, 'm', 3)
        '0,356 m'
        >>> round_fixed(0.035, 'V', 2)
        '0,035 V'
        >>> round_fixed(1200, 'Hz', 6, '.')
        '1200.00 Hz'
    """

    if any(char.isdecimal() for char in decimal):
        decimal = ","

    if unit != "":
        unit = " "+unit

    if precision == 0:
        return ""

    if mt.isnan(value):
        return "NaN"

    if value < 0:
        return "-"+round_fix(value=abs(value), unit=unit, precision=precision, decimal=decimal)

    if mt.isinf(value):
        return "inf"+unit

    sci_str = round_sci(value=value, unit='', precision=precision, decimal=decimal)

    if "×" not in sci_str:
        return sci_str + unit

    if not set(sci_str).intersection(set("⁻⁰¹²³⁴⁵⁶⁷⁸⁹")):
        num_exp = 1
    else:
        sci_exp_str = sci_str.split(" × 10")[1]
        for digit, symbol in zip(["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["⁻", "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]):
            sci_exp_str = sci_exp_str.replace(symbol, digit)
        num_exp = int(sci_exp_str)

    long_str = sci_str.split(" × 10")[0]

    if decimal not in long_str:
        long_str += decimal

    while num_exp != 0:
        dot_index = long_str.index(decimal)
        num_len = len(long_str)

        if num_exp > 0:
            if dot_index == num_len-1:
                long_str = long_str[:-1] + "0" + decimal
            else:
                char_after_dot = long_str[dot_index+1]
                long_str = long_str[:dot_index] + char_after_dot + decimal + long_str[dot_index+2:]
            num_exp -= 1
        else:
            if dot_index == 0:
                long_str = decimal + "0" + long_str[1:]
            elif dot_index == 1:
                char_before_dot = long_str[0]
                long_str = "0" + decimal + char_before_dot + long_str[2:]
            else:
                char_before_dot = long_str[dot_index-1]
                long_str = long_str[:dot_index-2] + decimal + char_before_dot + long_str
            num_exp += 1

    if long_str[-1] == decimal:
        long_str = long_str[:-1]

    return long_str + unit


def eng_formatter(unit: str = '', precision: int = 3, decimal: str = ',') -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função round_eng.

    Argumentos:
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        Função de formatação.

    Exemplos:
        >>> ax.xaxis.set_major_formatter(eng_formatter('V', 3))
    """

    def func(x, pos=None):
        return round_eng(value=x, unit=unit, precision=precision, decimal=decimal)
    return func


def sci_formatter(unit: str = '', precision: int = 3, decimal: str = ',', format: bool = True) -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função round_sci.

    Argumentos:
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        Função de formatação.

    Exemplos:
        >>> ax.xaxis.set_major_formatter(sci_formatter('V', 3))
    """

    def func(x, pos=None):
        return round_sci(value=x, unit=unit, precision=precision, decimal=decimal)
    return func


def fix_formatter(unit: str = '', precision: int = 3, decimal: str = ',', format: bool = True) -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função round_fix.

    Argumentos:
        -unit (str, opcional): Unidade a ser utilizada. Padrão: ''.
        -precision (int, opcional): Quantidade de algarismos significativos. Padrão: 3.
        -decimal (str, opcional): Caracter utilizado para separar o número inteiro e o número decimal. Se o separador contiver números, utiliza o padrão. Padrão: ','.

    Retorno:
        Função de formatação.

    Exemplos:
        >>> ax.xaxis.set_major_formatter(fix_formatter('V', 3))
    """

    def func(x, pos=None):
        return round_fix(value=x, unit=unit, precision=precision, decimal=decimal)
    return func


if __name__ == '__main__':
    print(round_eng(0.356, 'V', 3))
    print(round_sci(32000, 'Hz', 3, '.'))
    print(round_fix(0.32, 's', 3))
