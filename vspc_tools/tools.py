from to_precision import eng_notation as _eng_
from to_precision import sci_notation as _sci_

"""
Autor: Victor Sabiá Pereira Carpes
Descrição: Módulo com funções que eu utilizo o tempo inteiro.
"""

def eng_notation(value:float, unit:str='', precision:int=3, decimal:str=',', format:bool=True) -> str:
    """
    Formata um valor numérico utilizando os prefixos do SI para as potências de 10, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        -value: Valor a ser formatado.
        -unit: Unidade a ser utilizada. Padrão: ''.
        -precision: Quantidade de algarismos significativos. Padrão: 3.
        -decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
        -format: Flag que indica se o valor deve ser formatado ou não. Quando igual a False, a precisão equivale a casas depois da vírgula. Padrão: True.
    
    Retorno:
        -String formatada.
    
    Exemplos:
        >>> eng_notation(0.356, 'm', 3)
        '356 mm'
        >>> eng_notation(0.356, 'V', 2)
        '360 mV'
        >>> eng_notation(1200, 'Hz', 6, '.')
        '1.20000 kHz'
    """

    if format is not True:
        return f"{value:.{precision}f} {unit}".replace('.', decimal)
    string = _eng_(value, precision, 'E')
    string = string.replace('.E', 'E').replace('.', decimal)
    exps = ['E24', 'E21', 'E18', 'E15', 'E12', 'E9', 'E6', 'E3', 'E0', 'E-3', 'E-6', 'E-9', 'E-12', 'E-15', 'E-18', 'E-21', 'E-24']
    prefs = ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', '', 'm', 'μ', 'n', 'p', 'f', 'a', 'z', 'y']
    for (exp, pref) in zip(exps, prefs):
        string = string.replace(exp, ' '+pref)
    return string + unit

def eng_inv(string:str) -> float:
    """
    Converte uma string formatada em notação de engenharia para um valor numérico. 
    
    Argumentos:
        -string: String formatada. A string deve ser formatada utilizando apenas os prefixos do SI correspondentes às potências de 10 com expoente múltiplo de 3. Entre o valor numérico e a unidade é necessário um espaço. O separador decimal pode ser tanto ponto quanto vírgula. O prefixo micro (μ) deve ser digitado como 'u'.
    
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
    pref_dict = {'Y':24, 'Z':21, 'E':18, 'P':15, 'T':12, 'G':9, 'M':6, 'k':3, 'm':-3, 'u':-6, 'n':-9, 'p':-12, 'f':-15, 'a':-18, 'z':-21, 'y':-24}
    mantissa = mantissa.replace(',', '.')
    if len(unit) == 1 or unit[0] not in pref_dict:
        exponent = 0
    else:
        exponent = pref_dict[unit[0]]
    return float(mantissa) * 10**exponent


def sci_notation(value:float, unit:str='', precision:int=3, decimal:str=',', format:bool=True) -> str:
    """
    Formata um valor numérico utilizando em notação científica, utilizando a quantidade de algarismos significativos e unidade especificada.

    Argumentos:
        -value: Valor a ser formatado.
        -unit: Unidade a ser utilizada. Padrão: ''.
        -precision: Quantidade de algarismos significativos. Padrão: 3.
        -decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
        -format: Flag que indica se o valor deve ser formatado ou não. Quando igual a False, a precisão equivale a casas depois da vírgula. Padrão: True.
    
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

    if format is not True:
        return f"{value:.{precision}f} {unit}".replace('.', decimal)
    string = _sci_(value, precision, 'E')
    string = string.replace('.E', 'E').replace('.', decimal)
    mantissa, exponent = string.split('E')
    simbs = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    supers = ['⁻', '⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    if exponent == '0':
        return mantissa + ' ' + unit
    else:
        for (simb, super) in zip(simbs, supers):
            exponent = exponent.replace(simb, super)
    result = mantissa + ' × 10' + exponent + ' ' + unit
    result = result.replace('10¹', '10')
    return result

def eng_formatter(unit:str='', precision:int=3, decimal:str=',', format:bool=True) -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função eng_notation.

    Argumentos:
        -unit: Unidade a ser utilizada. Padrão: ''.
        -precision: Quantidade de algarismos significativos. Padrão: 3.
        -decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
        -format: Flag que indica se o valor deve ser formatado ou não. Quando igual a False, a precisão equivale a casas depois da vírgula. Padrão: True.
    
    Retorno:
        Função de formatação.
    
    Exemplos:
        >>> ax.xaxis.set_major_formatter(eng_formatter('V', 3))
    """

    def func(x, pos=None):
        return eng_notation(x, unit, precision, decimal, format)
    return func

def sci_formatter(unit:str='', precision:int=3, decimal:str=',', format:bool=True) -> callable:
    """
    Cria uma função de formatação para o uso com o módulo matplotlib que formata os labels dos eixos utilizando a função sci_notation.

    Argumentos:
        -unit: Unidade a ser utilizada. Padrão: ''.
        -precision: Quantidade de algarismos significativos. Padrão: 3.
        -decimal: Caracter utilizado para separar o número inteiro e o número decimal. Padrão: ','.
        -format: Flag que indica se o valor deve ser formatado ou não. Quando igual a False, a precisão equivale a casas depois da vírgula. Padrão: True.
    
    Retorno:
        Função de formatação.
    
    Exemplos:
        >>> ax.xaxis.set_major_formatter(sci_formatter('V', 3))
    """

    def func(x, pos=None):
        return sci_notation(x, unit, precision, decimal, format)
    return func



if __name__=='__main__':
    print(eng_notation(0.356, 'V', 3, format=False))
