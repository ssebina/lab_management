load database
     from sqlite:///app.db
     into postgresql:///tags

 with include drop, create tables, create indexes, reset sequences

  set work_mem to '16MB', maintenance_work_mem to '512 MB';