from HistoricalProfiles import post_hist_perfiles


def test_post_hist_perfiles():
    no_serie = "465P03"
    tipo_var = "2"
    tipo_dispo = "2"
    tipo_perfil = "1"
    fechaini = "2024-04-01"
    fechafin = "2024-04-01"
    json_perfiles = ""
    response = post_hist_perfiles(no_serie, tipo_var, tipo_dispo, tipo_perfil, fechaini, fechafin, json_perfiles)
    # print(response)
    # print(response['code'])
    # print(response['description'])
    print(response['valores'])


test_post_hist_perfiles()
