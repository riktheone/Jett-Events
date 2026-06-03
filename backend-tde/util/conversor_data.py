import datetime

formato_data = "%d/%m/%Y"
formato_data_hora = "%d/%m/%Y %H:%M"
formato_data_banco = "%Y-%m-%d %H:%M:%S"

def converterStringDataParaData(dataComoString):
    return datetime.datetime.strptime(dataComoString, formato_data)

def converterStringDoBancoDataParaData(dataComoString):
    return datetime.datetime.strptime(dataComoString, formato_data_banco)

def converterStringDataHoraParaData(dataComoString, horaComoString):
    if len(horaComoString) == 2:
        horaComoString = f"{horaComoString}:00"
    if len(horaComoString) != 5 or horaComoString[2] != ":":
        raise Exception("formato de hora inválido")
    return datetime.datetime.strptime(f"{dataComoString} {horaComoString}", formato_data_hora)
