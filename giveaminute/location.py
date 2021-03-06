"""
    :copyright: (c) 2011 Local Projects, all rights reserved
    :license: Affero GNU GPL v3, see LICENSE for more details.
"""

from framework.log import log
  
def getLocationsWithScoring(db):
    data = []
    
    log.info("*** hit locations")

    try:
        # TODO
        # this is temporary until actual scoring is determined
        sql = """
select l.location_id
    ,l.name
    ,l.lat
    ,l.lon
    ,(select count(*) as count
            from project p
            inner join project__user opu on opu.project_id = p.project_id and opu.is_project_admin = 1
            where
            p.is_active = 1 
            and p.location_id = l.location_id) as num_projects
    ,(select count(*) as count
            from idea i
            where
            i.is_active = 1
            and i.location_id = l.location_id) as num_ideas
    ,(select count(*) as count
            from project_resource r
            where
            r.is_active = 1 and r.is_hidden = 0 and r.location_id = l.location_id) as num_project_resources
from location l where l.location_id > 0""";
        data = list(db.query(sql))
    except Exception, e:
        log.info("*** couldn't get locations")
        log.error(e)

    return data 
        
def getLocations(db):
    data = []

    try:
        sql = """select l.location_id, l.name, l.lat, l.lon from location l where l.location_id > 0
                order by l.location_id""";
        data = list(db.query(sql))
    except Exception, e:
        log.info("*** couldn't get locations")
        log.error(e)

    return data 

def getLocationInfo(db, locationId):
    info = {}
    
    try:
        sql = """select 'n_projects' as key_name, count(*) as num from project where location_id = $id
union
select 'n_ideas' as key_name, count(*) as num from idea where location_id = $id
union
select 'n_resources' as key_name, count(*) as num from project_resource where location_id = $id;"""
        data = list(db.query(sql, {'id':locationId}))

        for item in data:
            info[item.key_name] = item.num
    except Exception, e:
        log.info("*** couldn't get location info")
        log.error(e)

    return info

# deprecated ?
def getSimpleLocationDictionary(db):
    data = getLocations(db)
    
    locations = []
    
    for item in data:
        locations.append({'name':item.name, 'location_id':item.location_id})
        
    return locations
    
    