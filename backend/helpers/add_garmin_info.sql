  alter table players.AUsers
  add HasGarmin bit

  update u
  set HasGarmin = 1
  from players.AUsers as u
  inner join rides.AGarminAthletes as g on u.Id = g.Id

  update u
  set HasGarmin = 0
  from players.AUsers as u
  where HasGarmin is null