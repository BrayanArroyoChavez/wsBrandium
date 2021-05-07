def getEmpresa(root,update):
    marca = root.select('div[data-test-id=item-detail-main] .sc-AxiKw.iIIwSC .bwtSwc div div')
    ant = ''
    for d in marca:
        if ant == '111 Número de registro':
            update[1] = d.text
        if ant == 'Tipo de DPI':
            update[2] = d.text
        if ant == '550 Tipo de marca':
            update[3] = d.text
        if ant == '511 Clasificación de Niza':
            update[4] = d.text
        
        ant = d.text
    return update

def getServicio(root,update):
    ps = root.select('span[data-test-id="goods-service-text"]')
    for d in ps:
        update[5] = update[5] + d.text
    return update

def getFecha(root, update):
    date = root.select('div[data-test-id="item-detail-dates"] .sc-AxiKw.grjojX .bwtSwc div div')
    ant = ''
    for d in date:
        if ant == '220 Fecha de solicitud':
            update[6] = "-".join(reversed(d.text.split("/"))) 
        if ant == '151 Fecha de registro':
            update[7] = "-".join(reversed(d.text.split("/"))) 
        if ant == '141 Fecha de vencimiento':
            update[8] = "-".join(reversed(d.text.split("/"))) 

        ant = d.text
    return update

def getSolicitante(root, update):
    solicitante = root.select('div[data-test-id="item-detail-owner"] .sc-AxiKw.grjojX .bwtSwc div div')
    ant = ''
    for d in solicitante:
        if ant == 'Nombre del solicitante':
            update[9] = d.text
        if ant == 'Ciudad':
            update[10] = d.text
        if ant == 'Dirección':
            update[11] = d.text
        if ant == 'País de incorporación':
            update[12] = d.text
        if ant == 'Teléfono':
            update[13] = d.text
        if ant == 'Correo electrónico':
            update[14] = d.text
        if ant == 'Código postal':
            update[15] = d.text

        ant = d.text
    return update

def getRepresentante(root, update):
    representante = root.select('div[data-test-id="item-detail-representative"] .sc-AxiKw.grjojX .bwtSwc div div')
    ant = ''
    for d in representante:
        if ant == 'Nombre':
            update[16] = d.text
        if ant == 'Dirección':
            update[17] = d.text
        if ant == 'Ciudad':
            update[18] = d.text
        if ant == 'Teléfono':
            update[19] = d.text
        if ant == 'Correo electrónico':
            update[20] = d.text
        if ant == 'Código postal':
            update[21] = d.text
        if ant == 'Código de la oficina':
            update[22] = d.text

        ant = d.text
    return update