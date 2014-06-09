import pyodbc

def getNumberOfManifests():
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	cursor.execute("select COUNT(*) FROM ent.ve_Message")
	rows = cursor.fetchall()
	return rows[0][0]

def getNumberOfContainers(manf_id):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	tmpquerry= "SELECT  COUNT(*) FROM [MYTNIK_CUSCAR].[ent].[ve_Container] where ManifestId = 'theID' "
	querry = tmpquerry.replace('theID', manf_id)
	cursor.execute(querry)
	rows = cursor.fetchall()
	return rows[0][0]

def getNumberOfBills(manf_id):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	tmpquerry = "SELECT  COUNT(*) from ent.ve_Message  inner join ent.ve_CargoDetails on ent.ve_Message.MessageId=ent.ve_CargoDetails.MessageId where ent.ve_Message.MessageId ='theID' "
	 
	querry = tmpquerry.replace('theID', manf_id)
	print querry
	cursor.execute(querry)
	rows = cursor.fetchall()
	return rows[0][0]

def getManifests(pagenum):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()

	querry = "select newtable.UnbReference , newtable.DocumentCreationTime , newtable.ArrivalTime , newtable.SenderId , newtable.OriginalSenderId , newtable.VesselName , newtable.VoyageNumber , newtable.RecipientId ,newtable.ContainerCount, newtable.PlFullCount , newtable.PlEmptyCount , newtable.TranshipmentCount from( SELECT ROW_NUMBER()       OVER (ORDER BY ent.ve_Message.UnbReference ) AS Row, ent.ve_Message.UnbReference , DocumentCreationTime , ArrivalTime , SenderId , OriginalSenderId , VesselName , VoyageNumber , RecipientId ,ContainerCount, PlFullCount , PlEmptyCount , TranshipmentCount  FROM ent.ve_Message INNER JOIN ent.ve_MessageContainerStatistics ON ent.ve_Message.MessageId=ent.ve_MessageContainerStatistics.messageId ) as newtable where newtable.Row >= MYMIN and newtable.Row < MYMAX order by newtable.UnbReference "
	tmp = querry.replace('MYMIN', str(pagenum * 20 + 1) )
	the_querry = tmp.replace('MYMAX', str( pagenum * 20 + 20 + 1 ))
	cursor.execute(the_querry)
	rows = cursor.fetchall()

	rowarray_list = []
	for row in rows:
	    t = (row.UnbReference, row.DocumentCreationTime, row.ArrivalTime, row.SenderId, row.OriginalSenderId, row.VesselName, row.VoyageNumber, row.RecipientId, row.ContainerCount,row.PlFullCount, row.PlEmptyCount, row.TranshipmentCount,)
	    rowarray_list.append(t)
	return rowarray_list

def getContainers_per_manifest(pagenum):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	pass

def getBills_per_manifest(pagenum, manf_id):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	ftmpquerry = """ 
				select newtable.UnbReference , newtable.BillofLading, newtable.OriginPort , newtable.LoadingPort , newtable.DischargePort
				from ( SELECT ROW_NUMBER() OVER (ORDER BY ent.ve_Message.UnbReference ) as ROW,ent.ve_Message.MessageId ,ent.ve_Message.UnbReference , BillofLading, OriginPort , LoadingPort , DischargePort
				from  ent.ve_Message  INNER JOIN ent.ve_CargoDetails on ent.ve_Message.MessageId=ent.ve_CargoDetails.MessageId where ent.ve_Message.MessageId='theID' )
				as newtable where newtable.Row >= MYMIN and newtable.Row < MYMAX order by newtable.UnbReference 
				"""
	stmpquerry = ftmpquerry.replace('theID', manf_id)
	ttmpquerry = stmpquerry.replace('MYMIN', str(pagenum * 20 + 1) )
	querry = ttmpquerry.replace('MYMAX', str( pagenum * 20 + 20 + 1 ))
	cursor.execute(querry)

	rows = cursor.fetchall()
	rowarray_list = []
	for row in rows:
		t = (row.UnbReference , row.BillofLading , row.OriginPort , row.LoadingPort , row.DischargePort)
		rowarray_list.append(t)
	return rowarray_list


def getSingleManifet(manf_id):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik;CHARSET=UTF8;unicode_results=False')
	cursor = cnxn.cursor()
	tmpquerry =""" SELECT [MessageId]
      ,[UnbReference]
      ,[SenderId]
      ,[RecipientId]
      ,[OriginalSenderId]
      ,[DocumentNumber]
      ,[DocumentCreationTime]
      ,[CarrierCode]
      ,[VoyageNumber]
      ,[VesselName]
      ,[ArrivalPort]
      ,[ArrivalTime]
  	FROM [MYTNIK_CUSCAR].[ent].[ve_Message] where [MessageId]='theID' """

  	querry = tmpquerry.replace('theID', manf_id)

	cursor.execute(querry)
	rows = cursor.fetchall()
	rowarray_list = []
	for row in rows:
		t = (row.MessageId , row.UnbReference ,row.SenderId ,row.RecipientId ,row.OriginalSenderId ,row.DocumentNumber ,row.DocumentCreationTime ,row.CarrierCode ,row.VoyageNumber ,row.VesselName ,row.ArrivalPort ,row.ArrivalTime , )
		rowarray_list.append(t)
	return rowarray_list

def getContainers():
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
	cursor = cnxn.cursor()
	querry = """select ent.ve_Message.UnbReference,  ent.ve_Container.ContainerIdentifier,  ent.ve_CargoDetails.BillofLading, CEILING (ent.ve_GoodsIdent.GoodsItemNumber) , ent.ve_Container.ContainerType, ent.ve_Container.ContainerStatus ,CEILING( ent.ve_Container.GrossWeightValue), ent.ve_Container.NetWeightValue, CEILING( ent.ve_Container.GrossVolumeValue ), ent.ve_GoodsIdent.PackagesDescType, CEILING ( ent.ve_GoodsIdent.GoodsItemNumber ), ent.ve_GoodsIdentFreeText.FreeTextLine1   from ent.ve_ContainerView
	inner join ent.ve_Message on ent.ve_ContainerView.MessageId = ent.ve_Message.MessageId
	inner join ent.ve_CargoDetails on ent.ve_ContainerView.CargoDetailsId = ent.ve_CargoDetails.CargoDetailsId
	inner join ent.ve_Container on ent.ve_ContainerView.ContainerId =  ent.ve_Container.ContainerId
	inner join ent.ve_GoodsIdent on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdent.GoodsIdentId
	INNER join ent.ve_GoodsIdentFreeText on ent.ve_ContainerView.GoodsIdentId = ent.ve_GoodsIdentFreeText.GoodsIdentId
	ORDER BY ent.ve_Message.UnbReference"""
	cursor.execute(querry)
	rows = cursor.fetchall()
	return rows

def getBills():
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
	cursor = cnxn.cursor()
	querry="""select UnbReference, BillofLading, OriginPort , LoadingPort , DischargePort from ent.ve_Message 
	inner join ent.ve_CargoDetails on ent.ve_Message.MessageId=ent.ve_CargoDetails.MessageId
	order by UnbReference""" 
	cursor.execute(querry)
	rows = cursor.fetchall()
	return rows