import sqlite3

DB_LOCATION = ("/Library/Containers/net.shinyfrog.bear/Data/Library/Application Support/net.shinyfrog.bear/database.sqlite")
MAS_DB_LOCATION = DB_LOCATION.replace('.dunno', '.dunno.MacAppStore')
DB_KEY = 'db_path'
# todo: need to figure out what the actual app store install location is

NOTE_TITLE_SEARCH = (
    "SELECT "
    "   ZUNIQUEIDENTIFIER, ZTITLE "
    "FROM "
    "   ZSFNOTE "
    "WHERE "
    "ZARCHIVED=0 "
    "AND ZTRASHED=0 "
    "AND lower(ZTITLE) LIKE lower('%{0}%')")

NOTE_TAG_SEARCH = (
    "SELECT "
        "n.ZUNIQUEIDENTIFIER, "
        "n.ZTITLE "
    "FROM "
        "ZSFNOTE n "
        "INNER JOIN ZSFNOTETAG t ON n.Z_PK = t.Z_PK "
    "WHERE "
        "n.ZARCHIVED=0 "
        "AND n.ZTRASHED=0 "
        "AND lower(n.ZTITLE) LIKE lower('%{0}%')")


def search_notes_by_title(wf, log, query):
    sqlQuery = NOTE_TITLE_SEARCH.format(query)
    #todo: search text as well as title, figure out best way to sort results
    return run_query(wf, log, sqlQuery)

def search_notes_by_tag(wf, log, query):
    sqlQuery = NOTE_TAG_SEARCH.format(query)
    return run_query(wf, log, sqlQuery)

def run_query(wf, log, sql):
  db_path = wf.stored_data(DB_KEY)
  if not db_path:
    db_path = find_bear_db(log)
    wf.store_data(DB_KEY, db_path)
  else:
    log.debug(db_path)

  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  log.debug(sql)
  cursor.execute(sql)
  results = cursor.fetchall()
  log.debug("Found {0} results".format(len(results)))
  cursor.close()
  return results

def find_bear_db(log):
  home = os.path.expanduser("~")
  db = "{0}{1}".format(home, DB_LOCATION)
  mas = "{0}{1}".format(home, MAS_DB_LOCATION)

  if not os.path.isfile(db):
      log.debug("Bear db not found at {0}; using {1} instead".format(db, mas))
      db = mas
  elif os.path.isfile(mas):
    db_mod = mod_date(db)
    mas_mod = mod_date(mas)
    if db_mod < mas_mod:
        db = mas
    log.debug("Bear direct and MAS db's found; using {0} as it's newer "
              "(Direct {1} vs. MAS {2})".format(db, db_mod, mas_mod))

  log.debug(db)
  return db


def mod_date(filename):
  mtime = os.path.getmtime(filename)
  return datetime.datetime.fromtimestamp(mtime)