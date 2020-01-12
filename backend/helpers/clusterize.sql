create table rides.Clusters (
	Id integer not null,
	MinLat float not null,
	MinLng float not null,
	MaxLat float not null,
	MaxLng float not null,
	constraint PK_Clusters primary key (Id)
)

select count(Id) from rides.Clusters
delete from rides.Clusters

  declare @maxLat float = 54.728265;
  declare @minLat float = 54.238511;
  declare @minLng float = 18.174628;
  declare @maxLng float = 18.951190;

  declare @latDiff float = @maxLat - @minLat;
  declare @lngDiff float = @maxLng - @minLng;
  declare @latStep float = @latDiff / 100;
  declare @lngStep float = @lngDiff / 100;

  declare @currentMinLat float = @minLat;
  declare @currentMinLng float = @minLng;
  declare @currentMaxLat float = @maxLat + @latStep;
  declare @currentMaxLng float = @maxLng + @lngStep;
  declare @i integer = 0;

    -- init table
  while @currentMinLat < @maxLat
  begin
  	while @currentMinLng < @maxLng
	begin
		insert into rides.Clusters values (@i, 0,0,0,0);
		set @i = @i + 1;
		set @currentMinLng = @currentMinLng + @lngStep;
		set @currentMaxLng = @currentMaxLng + @lngStep;
	end;
	set @currentMinLng = @minLng;
	set @currentMaxLng = @minLng + @lngStep;
	set @currentMinLat = @currentMinLat + @latStep;
	set @currentMaxLat = @currentMaxLat + @latStep;
  end;
  print @i;


  -- create clusters
  set @currentMinLat = @minLat;
  set @currentMinLng = @minLng;
  set @currentMaxLat = @maxLat + @latStep;
  set @currentMaxLng = @maxLng + @lngStep;
  set @i = 0;

  while @currentMinLat < @maxLat
  begin
  	while @currentMinLng < @maxLng
	begin

		update rides.Clusters
		set MinLat = @currentMinLat, MinLng = @currentMinLng, MaxLat = @currentMaxLat, MaxLng = @currentMaxLng
		where Id = @i;

		set @i = @i + 1;
		set @currentMinLng = @currentMinLng + @lngStep;
		set @currentMaxLng = @currentMaxLng + @lngStep;
	end;
	set @currentMinLng = @minLng;
	set @currentMaxLng = @minLng + @lngStep;
	set @currentMinLat = @currentMinLat + @latStep;
	set @currentMaxLat = @currentMaxLat + @latStep;
	print @i
  end;


  create table rides.CluseteredRides (
    Id uniqueidentifier not null,
	ClusterId integer not null,
	RideId uniqueidentifier not null,
	Lat float not null,
	Lng float not null,
	Start bit not null,
	constraint PK_ClusteredRides primary key (Id),
	constraint FK_ClusteredRides_Clusters foreign key (ClusterId) references rides.Clusters(Id),
	constraint FK_ClusteredRides_Rides foreign key (RideId) references rides.ARides(Id)
)


  --clusterize rides
  declare @j integer = 0;

  while @j < 10000
  begin
	with cluster as (
		select Id as Id, MinLat as MinLat, MaxLat as MaxLat, MinLng as MinLng, MaxLng as MaxLng
		from rides.Clusters
		where Id = @j
	),
	ridesStart as (
		select Id as RideId, StartLocation_Latitude as Lat , StartLocation_Longitude as Lng, 1 as Start
		from rides.ARides
		where StartLocation_Latitude >= (select MinLat from cluster) and StartLocation_Latitude < (select MaxLat from cluster)
		and StartLocation_Longitude >= (select MinLng from cluster) and StartLocation_Longitude < (select MaxLng from cluster)
	),
	ridesEnd as (
		select Id as RideId, EndLocation_Latitude as Lat, EndLocation_Longitude as Lng, 0 as Start
		from rides.ARides
		where EndLocation_Latitude >= (select MinLat from cluster) and EndLocation_Latitude < (select MaxLat from cluster)
		and EndLocation_Longitude >= (select MinLng from cluster) and EndLocation_Longitude < (select MaxLng from cluster)
	),
	rides as (
		select * from ridesStart
		union
		select * from ridesEnd
	)
	insert into rides.CluseteredRides select NEWID(), @j, RideId, Lat, Lng, Start from rides;
  end;