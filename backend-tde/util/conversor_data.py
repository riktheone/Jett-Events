import datetime

formato_data = "%d/%m/%Y"
formato_data_iso = "%Y-%m-%d"
formato_data_hora = "%d/%m/%Y %H:%M"
formato_data_hora_iso = "%Y-%m-%d %H:%M"
formato_data_banco = "%Y-%m-%d %H:%M:%S"


def converterStringDataParaData(dataComoString):
    if isinstance(dataComoString, datetime.datetime):
        return dataComoString
    if isinstance(dataComoString, datetime.date):
        return datetime.datetime.combine(dataComoString, datetime.time.min)

    valor = str(dataComoString).strip().replace("T", " ")
    for formato in (formato_data_banco, formato_data_hora_iso, formato_data_iso, formato_data):
        try:
            return datetime.datetime.strptime(valor, formato)
        except ValueError:
            pass
    raise ValueError(f"formato de data invalido: {dataComoString}")


def converterStringDoBancoDataParaData(dataComoString):
    return converterStringDataParaData(dataComoString)


def converterStringDataHoraParaData(dataComoString, horaComoString):
    if isinstance(horaComoString, datetime.datetime):
        return horaComoString

    horaComoString = str(horaComoString).strip()
    if " " in horaComoString:
        return converterStringDataParaData(horaComoString)
    if len(horaComoString) == 2:
        horaComoString = f"{horaComoString}:00"
    if len(horaComoString) == 8 and horaComoString[2] == ":":
        horaComoString = horaComoString[:5]
    if len(horaComoString) != 5 or horaComoString[2] != ":":
        raise Exception("formato de hora invalido")

    data = converterStringDataParaData(dataComoString)
    return datetime.datetime.strptime(f"{data.strftime('%Y-%m-%d')} {horaComoString}", formato_data_hora_iso)
