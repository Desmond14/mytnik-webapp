import pyodbc

def getManifests():
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=MYTNIK_CUSCAR;UID=mytnik;PWD=mytnik')
	cursor = cnxn.cursor()
	cursor.execute("select UnbReference, DocumentCreationTime, ArrivalTime, SenderId ,OriginalSenderId , VesselName , VoyageNumber , RecipientId, ent.ve_MessageContainerStatistics.ContainerCount, ent.ve_MessageContainerStatistics.PlFullCount, ent.ve_MessageContainerStatistics.PlEmptyCount, ent.ve_MessageContainerStatistics.TranshipmentCount from ent.ve_Message inner join ent.ve_MessageContainerStatistics on ent.ve_Message.MessageId=ent.ve_MessageContainerStatistics.messageId")
	rows = cursor.fetchall()
	return rows

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