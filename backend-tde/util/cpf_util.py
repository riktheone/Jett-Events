def limpar_cpf(cpf):
    return ''.join(filter(str.isdigit, str(cpf or '')))[:11]
