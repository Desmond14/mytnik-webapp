import pyodbc
from webint.models import ContainerStatus


def get_manifests():
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
    cursor = cnxn.cursor()
    cursor.execute(
        "select UnbReference  AS a , DocumentCreationTime  AS b , ArrivalTime AS c , SenderId AS d  ,OriginalSenderId  AS e , VesselName AS f , VoyageNumber AS g  , RecipientId AS h, ent.ve_MessageContainerStatistics.ContainerCount AS i, ent.ve_MessageContainerStatistics.PlFullCount AS j, ent.ve_MessageContainerStatistics.PlEmptyCount AS k, ent.ve_MessageContainerStatistics.TranshipmentCount AS l from ent.ve_Message inner join ent.ve_MessageContainerStatistics on ent.ve_Message.MessageId=ent.ve_MessageContainerStatistics.messageId")
    rows = cursor.fetchall()

    rowarray_list = []
    for row in rows:
        t = (row.a, row.b, row.c, row.d, row.e, row.f, row.g, row.h, row.i, row.j, row.k, row.l,)
        rowarray_list.append(t)
    return rowarray_list


def get_containers_per_manifest(pagenum, manf_id):
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
    cursor = cnxn.cursor()
    ftmpquerry = """ select newtable.MessageId ,newtable.UnbReference,  newtable.ContainerIdentifier,  newtable.BillofLading, CEILING (newtable.goodsitem) as goods , newtable.ContainerType, newtable.ContainerStatus ,CEILING( newtable.grossweightvla) as b, newtable.NetWeightValue, CEILING( newtable.grossvolval ) as c, newtable.PackagesDescType, CEILING ( newtable.goodsitemnumber ) as ww, newtable.FreeTextLine1
from ( select ROW_NUMBER() OVER (ORDER BY ent.ve_Message.UnbReference ) as ROW ,ent.ve_Message.MessageId ,ent.ve_Message.UnbReference,  ent.ve_Container.ContainerIdentifier,  ent.ve_CargoDetails.BillofLading, CEILING (ent.ve_GoodsIdent.GoodsItemNumber) as goodsitem , ent.ve_Container.ContainerType, ent.ve_Container.ContainerStatus ,CEILING( ent.ve_Container.GrossWeightValue) as grossweightvla, ent.ve_Container.NetWeightValue, CEILING( ent.ve_Container.GrossVolumeValue ) as grossvolval, ent.ve_GoodsIdent.PackagesDescType, CEILING ( ent.ve_GoodsIdent.GoodsItemNumber ) as goodsitemnumber, ent.ve_GoodsIdentFreeText.FreeTextLine1   from ent.ve_ContainerView
	inner join ent.ve_Message on ent.ve_ContainerView.MessageId = ent.ve_Message.MessageId
	inner join ent.ve_CargoDetails on ent.ve_ContainerView.CargoDetailsId = ent.ve_CargoDetails.CargoDetailsId
	inner join ent.ve_Container on ent.ve_ContainerView.ContainerId =  ent.ve_Container.ContainerId
	inner join ent.ve_GoodsIdent on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdent.GoodsIdentId
	INNER join ent.ve_GoodsIdentFreeText on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdentFreeText.GoodsIdentId
	where ent.ve_Message.MessageId ='theID' ) as newtable where newtable.Row >= MYMIN and newtable.Row < MYMAX 
	 """
    stmpquerry = ftmpquerry.replace('theID', manf_id)
    ttmpquerry = stmpquerry.replace('MYMIN', str(pagenum * 20 + 1))
    querry = ttmpquerry.replace('MYMAX', str(pagenum * 20 + 20 + 1))
    cursor.execute(querry)

    rows = cursor.fetchall()
    rowarray_list = []
    for row in rows:
        t = (row.MessageId, row.UnbReference, row.ContainerIdentifier, row.BillofLading, row.goods, row.ContainerType,
             row.ContainerStatus, row.b, row.NetWeightValue, row.c, row.PackagesDescType, row.ww, row.FreeTextLine1)
        rowarray_list.append(t)
    return rowarray_list


def get_containers_with_status():
    simple_containers = get_simple_containers()
    containers_with_status = []
    for container in simple_containers:
        container_id = container.b
        try:
            status = ContainerStatus.objects.get(container_id=container_id)
        except ContainerStatus.DoesNotExist:
            status = ContainerStatus(container_id=container_id)
            print "Created Status for container " + container_id
            status.save()
        resulting_container = (
            str(container.a), str(container.b), str(container.c), str(container.d),
            str(status.status), str(status.assignee))
        containers_with_status.append(resulting_container)
    return containers_with_status


def get_simple_containers():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
    cursor = cnxn.cursor()
    querry = """select UnbReference as a,ContainerIdentifier as b,ContainerType as c, ContainerLoad as d from ent.ve_Message inner join ent.ve_Container on ve_Message.MessageId = ve_Container.ManifestId"""
    cursor.execute(querry)
    rows = cursor.fetchall()
    # res = []
    # for row in rows:
    #     t=(row.a, row.b, row.c, row.d)
    #     res.append(t);
    # print len(rows)
    # return res
    return rows

def get_containers():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
    cursor = cnxn.cursor()
    querry = """select ent.ve_Message.UnbReference as a,  ent.ve_Container.ContainerIdentifier as b,  ent.ve_CargoDetails.BillofLading as c, CEILING (ent.ve_GoodsIdent.GoodsItemNumber) as d , ent.ve_Container.ContainerType as e, ent.ve_Container.ContainerStatus as f,CEILING( ent.ve_Container.GrossWeightValue) as g, ent.ve_Container.NetWeightValue as h, CEILING( ent.ve_Container.GrossVolumeValue ) as i, ent.ve_GoodsIdent.PackagesDescType as j, CEILING ( ent.ve_GoodsIdent.GoodsItemNumber ) as k, ent.ve_GoodsIdentFreeText.FreeTextLine1 as l from ent.ve_ContainerView
	inner join ent.ve_Message on ent.ve_ContainerView.MessageId = ent.ve_Message.MessageId
	inner join ent.ve_CargoDetails on ent.ve_ContainerView.CargoDetailsId = ent.ve_CargoDetails.CargoDetailsId
	inner join ent.ve_Container on ent.ve_ContainerView.ContainerId =  ent.ve_Container.ContainerId
	inner join ent.ve_GoodsIdent on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdent.GoodsIdentId
	INNER join ent.ve_GoodsIdentFreeText on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdentFreeText.GoodsIdentId
	ORDER BY ent.ve_Message.UnbReference"""
    cursor.execute(querry)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        t=(row.a, row.b, row.c, str(row.d), row.e, row.f, str(row.g), str(row.h), str(row.i), row.j, str(row.k), row.l)
        res.append(t);
    return res


def get_bills():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
    cursor = cnxn.cursor()
    querry = """select UnbReference as a, BillofLading as b, OriginPort as c , LoadingPort as d, DischargePort as e from ent.ve_Message
	inner join ent.ve_CargoDetails on ent.ve_Message.MessageId=ent.ve_CargoDetails.MessageId
	order by UnbReference"""
    cursor.execute(querry)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        t=(row.a, row.b, row.c, row.d, row.e)
        res.append(t);
    return res


def get_bills_for_container(ContainerId):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
    cursor = cnxn.cursor()
    ftmpquerry = """select  a.ContainerIdentifier as f, b.BillofLading as g, b.OriginPort as h, b.LoadingPort as i, b.DischargePort as j, c.CityName as k, c.Country as l, c.NameAndAddressId as m from ent.ve_ContainerView
	inner join  ent.ve_Container as a on ent.ve_ContainerView.ContainerId=a.ContainerId
	inner join  ent.ve_CargoDetails as b on ent.ve_ContainerView.CargoDetailsId=b.CargoDetailsId
	inner join  ent.ve_CargoDetailsNameAndAddress as c on b.CargoDetailsId=c.CargoDetailsId
	where a.ContainerIdentifier='theID' 
	"""
    querry = ftmpquerry.replace('theID', ContainerId)
    print querry
    cursor.execute(querry)
    rows = cursor.fetchall()
    res = []
    for row in rows:
        t=(row.f, row.g, row.h, row.i, row.j, str(row.k), str(row.l), row.m)
        res.append(t);
    return res

def rule_parser(dict_to_parse):
    parsed_dict ={}
    res = []    
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
    cursor = cnxn.cursor()
    basequerry = """select * from ent.ve_ContainerView as maintable
    inner join  ent.ve_CargoDetails  on ent.ve_CargoDetails.CargoDetailsId=maintable.CargoDetailsId
    inner join  ent.ve_Message  on  ent.ve_Message.MessageId=maintable.MessageId
    inner join  ent.ve_Container   on ent.ve_Container.ContainerId=maintable.ContainerId
    inner join  ent.ve_GoodsIdent   on ent.ve_GoodsIdent.GoodsIdentId=maintable.GoodsIdentId
    where """
    for rule, rule_dict in dict_to_parse.iteritems():
        tmpquerry = basequerry
        if rule_dict['filter_type'] == 'AND':
            for column_filter, value in rule_dict['filters'].iteritems():
                #tmpquerry = tmpquerry + str(column_filter) + " like " + " '" + str(value) + "' " + " and "
                                          ### Column filter       ### operator       ### value
                tmpquerry = tmpquerry + str(column_filter) + " "+ value[0] + " '" + str(value[1]) + "' " + " and "
            # removing last and
            tmpquerry = tmpquerry[:-4]
            cursor.execute(tmpquerry)
            rows = cursor.fetchall()
            for row in rows:
                t=(row[1],row[6],row[7],row[8],row[9],row[10],row[32],rule_dict['severity'])
                res.append(t);
        if rule_dict['filter_type'] == 'OR':
            for column_filter, value in rule_dict['filters'].iteritems():
                #tmpquerry = tmpquerry + str(column_filter) + " like " + " '" + str(value) + "' " + " or "
                                          ### Column filter       ### operator       ### value
                tmpquerry = tmpquerry + str(column_filter) + " "+ value[0] + " '" + str(value[1]) + "' " + " or "
            # removing last or
            tmpquerry = tmpquerry[:-4]
            cursor.execute(tmpquerry)
            rows = cursor.fetchall()
            for row in rows:
                t=(row[1],row[6],row[7],row[8],row[9],row[10],row[32],rule_dict['severity'])
                res.append(t);
    parsed_dict['returned_list'] = res
    return parsed_dict

def combine_serevity(list_to_combine):
    counter = {}
    which_containers_combine_severity = []
    print "Helloo"
    for single_tuple in list_to_combine:
        counter[single_tuple[0]]=0
    for single_tuple in list_to_combine:
        counter[single_tuple[0]]+=1
    for container_id, liczba_wystapien in counter.iteritems():
        if liczba_wystapien >=2:
            which_containers_combine_severity.append(container_id)
    for id_ in which_containers_combine_severity:
        summary_sev = 0
        list_of_indexes = []
        list_of_indexes_to_be_removed = []
        for i in range(len(list_to_combine)):
            if  list_to_combine[i][0] == id_:
                 list_of_indexes.append(i)
        for instace in range(len(list_of_indexes)):
            if instace >= 1:
                list_to_combine[list_of_indexes[0]][7] += list_to_combine[list_of_indexes[instace]][7]
                list_of_indexes_to_be_removed.append(list_of_indexes[instace])
        offset=0
        for removed_index in list_of_indexes_to_be_removed:
            list_to_combine.pop(removed_index-offset)
            print removed_index
            offset+=1
    return list_to_combine





