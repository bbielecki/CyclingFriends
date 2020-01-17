create table rides.Pois (
	Id integer not null IDENTITY(1,1),
    ClusterId integer not null,
	Lat float not null,
	Lng float not null,
    Tags NVARCHAR(max),
	constraint PK_Pois primary key (Id),
)
