CREATE DATABASE electric;
GO
USE electric;
GO
CREATE TABLE poolprice
(
  pool_time_stamp datetime not null,
  pool_price decimal(6,2),
  forecast_pool_price decimal(6,2),
  insert_time_stamp datetime,
  update_time_stamp datetime,
  constraint pk_pooltimestamp primary key clustered (pool_time_stamp)
);
CREATE TABLE poolstage
(
  pool_time_stamp datetime not null,
  pool_price decimal(6,2),
  forecast_pool_price decimal(6,2),
  insert_time_stamp datetime,
  constraint pk_poolstagetimestamp primary key clustered (pool_time_stamp)
);

GO