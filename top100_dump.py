import pypyodbc
from app import db, models


# TD query, get relevant statistics
conn_td = pypyodbc.connect('DSN=blahblah;UID=blablahblah;PWD=blahblahblahblah1234')

cursor = conn_td.cursor()
sql = """ SELECT  top 100
                     DB.ProcID,
                     CASE WHEN DB.QueryID = 0 THEN 0 ELSE ((DB.ProcID / 100000)*10000000000)+ DB.QueryID END AS QueryID,
                     UserName, 
                     SessionID, 
                     AppID,
                     ClientID,
                     FirstRespTime AS LastRespTime,
                     
                     CAST( ((FirstRespTime - starttime) HOUR(2) TO SECOND) AS VARCHAR(50)) (NAMED ElapsedTime),
                     (DELAYTIME/60) AS DELAY_IN_MINS ,
                     NumSteps,
                     TotalIOCount,
                     AMPCPUTime + ParserCPUTime AS TotalCPUTime ,
                     
                     CASE WHEN((DB.AMPCPUTime/NULLIF(DB.NumOfActiveAMPs,0))/NULLIF(DB.MaxAMPCPUTime,0))  > 1 THEN NULL ELSE (1-(DB.AMPCPUTime/NULLIF(DB.NumOfActiveAMPs,0))/NULLIF (DB.MaxAMPCPUTime,0)) * 100  END AS CPU_Skew,
                     
                     CASE WHEN((DB.TotalIOCount/NULLIF(DB.NumOfActiveAMPs,0))/NULLIF (DB.MaxAmpIO,0))     > 1 THEN NULL ELSE (1-(DB.TotalIOCount/NULLIF(DB.NumOfActiveAMPs,0))/NULLIF (DB.MaxAmpIO,0)) * 100     END AS IO_Skew,
                                             
                     SpoolUsage,
                     (AMPCPUTIME * 1000) / TOTALIOCOUNT AS PJI,
                     TOTALIOCOUNT / (TOTALCPUTIME * 1000)AS UII,
                     SqlTextInfo


                FROM SYS_V_USR.DBQLogTbl_hst  DB

                LEFT OUTER JOIN

                SYS_V_USR.DBQLSqlTbl_Hst SQ

                ON DB.QueryID = SQ.QueryID
                AND DB.PROCID = SQ.PROCID

              
                
                WHERE
                
                TOTALCPUTIME > 0
                AND TOTALIOCOUNT>0

                AND errortext is null
                AND DB.logdate = '2014-06-25'
                ORDER BY TotalCPUTime DESC """

cursor.execute(sql)


# dumping TD results into local DB
for row in cursor.fetchall():
    insert = models.Query(

    proc_id = str(row[0]).strip(),
    query_id = str(row[1]).strip(),
    user_name = str(row[2]).strip(),
    session_id = str(row[3]).strip(),
    app_id = str(row[4]).strip(),
    client_id = str(row[5]).strip(),
    last_resp_time = str(row[6]).strip(),
    elapsed_time = str(row[7]).strip(),
    delay_in_minutes = str(row[8]).strip(),
    num_steps = str(row[9]).strip(),
    total_io_count = row[10],
    total_cpu_time = row[11],
    cpu_skew = row[12],
    io_skew = row[13],
    spool_usage = row[14],
    pji = row[15],
    uii = row[16],
    sql = str(row[17]).strip(),
    status = 'Not Assigned',
    assigned = 0)
    
    db.session.add(insert)
    db.session.commit()



cursor.close()
conn_td.close()