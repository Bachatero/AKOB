
CREATE OR REPLACE 
PACKAGE                 dwh_adm.pkg_set_stats
  IS

  pkc_process_name    CONSTANT    VARCHAR2(50) := 'DWH_APP';
  pkc_subprocess_name CONSTANT    VARCHAR2(100):= 'SET_STATS';
  pkc_package         CONSTANT    VARCHAR2(30) := 'PKG_SET_STATS';


    procedure p_gather_stats_ibachateronc(p_stat_mode varchar2);
    procedure p_run_gather_stats_inc (p_owner varchar2, p_table_name varchar2, p_granularity varchar2, p_subobject_name varchar2 default NULL);

    procedure p_set_object_stats(p_table_name varchar2 default null, p_table_owner varchar2 default null, p_backup_global BOOLEAN default null);
    procedure p_get_partition_key_column(pp_table_name in dba_tables.table_name%type,pp_owner in dba_tables.owner%type, pp_part_key OUT
            dba_part_key_columns.column_name%type, pp_part_key_type OUT dba_tab_columns.data_type%TYPE );
    procedure p_set_column_stats(pp_table_name in dba_tables.table_name%type,pp_owner in dba_tables.owner%type,
        pp_partition_name IN dba_tab_partitions.partition_name%type, pp_part_key IN dba_part_key_columns.column_name%type
        , pp_part_key_type IN dba_tab_columns.data_type%TYPE);

    procedure p_set_col_stats(pp_table_name in dba_tables.table_name%TYPE,pp_owner in dba_tables.owner%TYPE,pp_stat_type varchar2,
        pp_partition_name IN dba_tab_partitions.partition_name%TYPE,pp_src_partition_name IN dba_tab_partitions.partition_name%TYPE default NULL,
        pp_part_key IN dba_part_key_columns.column_name%TYPE, pp_part_key_type IN dba_tab_columns.data_type%TYPE);

    procedure p_send_mail(p_vystup_file IN clob, p_mail_subj varchar2);

END pkg_set_stats;
/

-- Grants for Package
GRANT EXECUTE ON dwh_adm.pkg_set_stats TO public
/

CREATE OR REPLACE 
PACKAGE BODY                 dwh_adm.pkg_set_stats
IS
    --x_bachatero


   procedure p_gather_stats_inc (p_stat_mode varchar2) IS

        pv_procname    CONSTANT VARCHAR2(30) := 'GATHER_STATS_INC';

   BEGIN

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'Start Stats Gathering',
                                   'INSERT INTO dwh_adm.TBL_STATS_INC');


        IF p_stat_mode = 'NO_STAT' then
            INSERT INTO dwh_adm.TBL_STATS_INC
            SELECT owner as table_owner, table_name, null as partition_name, null as subpartition_name FROM dba_tables
            WHERE (table_name, owner) IN (SELECT table_name, owner FROM DBA_TAB_STAT_PREFS)
            AND last_analyzed IS NULL
            UNION
            SELECT table_owner, table_name, partition_name, null AS subpartition_name FROM dba_tab_partitions
            WHERE (table_name, table_owner) IN (SELECT table_name, owner FROM DBA_TAB_STAT_PREFS)
            AND last_analyzed IS NULL
            UNION
            SELECT table_owner, table_name, partition_name, subpartition_name FROM dba_tab_subpartitions
            WHERE (table_name, table_owner) IN (SELECT table_name, owner FROM DBA_TAB_STAT_PREFS)
            AND last_analyzed IS NULL;
        ELSIF p_stat_mode = 'STALE_STAT' then
            INSERT INTO dwh_adm.TBL_STATS_INC
            SELECT DISTINCT owner , table_name,  partition_name,  subpartition_name
            FROM dba_tab_statistics
            WHERE (table_name, owner) IN (SELECT table_name, owner FROM DBA_TAB_STAT_PREFS)
            AND   stattype_locked IS NULL  AND stale_stats = 'YES' AND table_name NOT LIKE 'BIN%';
        END IF;


        FOR c_sp IN (SELECT owner, table_name, partition_name, subpartition_name
              from dwh_adm.TBL_STATS_INC
              where subpartition_name IS NOT NULL ) LOOP
            p_run_gather_stats_inc(c_sp.owner,c_sp.table_name, 'SUBPARTITION', c_sp.subpartition_name);
        END LOOP;


        FOR c_p IN (SELECT DISTINCT owner, table_name, partition_name
              FROM dwh_adm.TBL_STATS_INC
              WHERE partition_name IS NOT NULL AND subpartition_name IS NULL ) LOOP
            p_run_gather_stats_inc(c_p.owner,c_p.table_name, 'PARTITION', c_p.partition_name);
        END LOOP;


        FOR c_t IN (SELECT DISTINCT owner, table_name
              FROM dwh_adm.TBL_STATS_INC ) LOOP
            p_run_gather_stats_inc(c_t.owner,c_t.table_name,'GLOBAL');
        END LOOP;

        COMMIT;

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'Gather Stats',
                                   'END '|| p_stat_mode ||' Stats Gathering');

   END p_gather_stats_inc;


   procedure p_run_gather_stats_inc (p_owner varchar2, p_table_name varchar2, p_granularity varchar2, p_subobject_name varchar2 default NULL) IS

        c_head varchar2(60):= 'begin dbms_stats.gather_table_stats(''';
        c_opts varchar2(300):= ''',method_opt=>''FOR ALL COLUMNS size auto'', estimate_percent => SYS.DBMS_STATS.AUTO_SAMPLE_SIZE,degree=>SYS.DBMS_STATS.AUTO_DEGREE, cascade=>true); end;';
        pv_procname    CONSTANT VARCHAR2(30) := 'RUN_GATHER_STATS_INC';

   BEGIN
        IF p_owner IS NOT NULL THEN
            IF p_subobject_name IS NOT NULL THEN
                execute immediate c_head||''||p_owner||''', '''||p_table_name||''','''||p_subobject_name||''',granularity =>'''||p_granularity || ''|| c_opts;
            ELSE
                execute immediate c_head||''||p_owner||''', '''||p_table_name||''',granularity =>'''||p_granularity || ''|| c_opts;
            END IF;
        END IF;
   END p_run_gather_stats_inc;




   procedure p_set_object_stats_old(p_table_name varchar2 default null, p_table_owner varchar2 default null, p_backup_global boolean default null) IS

        pv_procname         CONSTANT VARCHAR2(30) := 'SET_OBJECT_STATS';
        pv_src_part dba_tab_partitions.partition_name%type;
        --pv_last_part        dba_tab_partitions.partition_name%type;
        --pv_no_partitions    dba_tab_partitions.partition_position%type;
        pv_no_rows          dba_tab_partitions.num_rows%type := NULL;
        pv_no_blocks        dba_tab_partitions.blocks%type := NULL;
        pv_global_rows      number;
        pv_global_blocks    number;
        pv_not_null_parts   number; --pocet particii s poctom riadkov vacsim ako avg vsetkych particii
        pv_random_val       number;

   BEGIN
        --return;
        --TODO: 1. subpartitions --nothing to solve
        --      2. set individual tables/partitions called from within dwh_adm loading jobs
        --      3. while using real scale_factor other than 1 do round num_rows to integer
        --      4. backup global stats --done
        --scale factor nerobi automaticky round poctu riadkov, pocet nie je cele cislo !
        --global stats mesacny num rows a blocks zo suctu particiovych num_rows a blocks
        --alebo sucet poslednej particie a aktual global stats
        --!!! zatial iba particionovane tabulky, bez tabuliek subpartitiovanych !!!
        --nastavene iba konkretne tabulky, ktore uz historicke stats maju

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'Start Stats Setting',
                                   'Loop tables START');
        /*
        FOR c_t IN (SELECT table_owner, table_name, scale_factor
                     FROM dwh_adm.TBL_SET_STAT_TABS
                     WHERE active = 'Y' ) LOOP
        */
        --loop najnovsich particii, kt. su zaroven bez statistik
        FOR c_t IN ( SELECT a.table_owner, a.table_name, a.scale_factor, b.partition_name, b.partition_position
                     FROM dwh_adm.TBL_SET_STAT_TABS a, dba_tab_partitions b
                     WHERE a.table_owner = b.table_owner AND a.table_name = b.table_name
                     AND a.active = 'Y' AND (b.last_analyzed IS NULL OR b.num_rows IS NULL)
                     AND b.partition_position = (SELECT max(partition_position)
                                                 FROM dba_tab_partitions c
                                                 WHERE c.table_name = a.table_name
                                                 AND c.table_owner = a.table_owner
                                                 --pridane kvoli MAX_VALUE particiam, ktore maju vzdy najvyssiu partition_position
                                                 AND c.partition_name not like '%MAX%'
                                                ))
        LOOP
            dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname
                                   ,'Start',
                                   substr(c_t.table_owner || '.' || c_t.table_name||'.'||c_t.partition_name,1,100));


            --getni meno poslednej particie s null stats
            --pouzitie dba_tab_partitions, pretoze selekt z dba_tab_statistics je pomalsi
            /*
            SELECT partition_name, partition_position
            INTO pv_last_part, pv_no_partitions
            FROM  dba_tab_partitions
            WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
            AND partition_position = (SELECT max(partition_position)
                                      FROM dba_tab_partitions
                                      WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner );
            */

            --ak je scale factor > 1, getni last but one partition name - predposlednu particiu, its num_rows & blocks
            --scale_factor= 1 or scale_factor > 1
            IF  c_t.scale_factor > 1 THEN
                SELECT partition_name, num_rows, blocks
                INTO pv_src_part, pv_no_rows, pv_no_blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                AND partition_position = c_t.partition_position - 1;
            ELSE --ak je scale 1, t.z. ze raz je v particii vacsi, inokedy mensi pocet riadkov ,
                -->vyber  nahodne jednu not null/not zero particiu ako zdrojovu a tu skopiruj do target
                /*
                SELECT partition_name, num_rows, blocks
                INTO pv_src_part, pv_no_rows, pv_no_blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                AND partition_position = (SELECT round(dbms_random.value(1, c_t.partition_position -1 )) from dual);
                */
                --najprv insertni do temp tabulky nenulove particie s poctom num_rows vacsim ako priemer (kvoli aktualnym particiam, resp.
                --particiam, ktore su vytvorene 3 mesiace dopredu ako je aktualny run_date a je v nich insertnutych len par riadkov)
                --a potom nahodne vyber jednu z nich  a jej stats skopiruj do aktualnej target.
                EXECUTE IMMEDIATE 'truncate table dwh_adm.tbl_set_stats';

                INSERT INTO dwh_adm.tbl_set_stats
                SELECT rownum, table_owner,table_name,partition_name, num_rows, blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                --AND num_rows IS NOT null and num_rows <> 0;
                AND num_rows >= (SELECT avg(num_rows)FROM  dba_tab_partitions
                                 WHERE table_name = c_t.table_name
                                 AND table_owner = c_t.table_owner);

                pv_not_null_parts:=SQL%rowcount;

                IF   pv_not_null_parts > 0 THEN
                    SELECT partition_name, no_rows, no_blocks
                    INTO  pv_src_part, pv_no_rows, pv_no_blocks
                    FROM  dwh_adm.tbl_set_stats
                    WHERE  id_row =(SELECT round(dbms_random.value(1, pv_not_null_parts ))  FROM dual);
                ELSE
                    --posli mail !!!, ze nema co nasetovat/skopirovat & zavolaj klasicke pocitanie stats

                    dwh_adm.pkg_adm_log.p_do_error(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname
                                   ,'Neexistuje nenulova source particia',
                                   substr(c_t.table_owner || '.' || c_t.table_name,1,100));

                END IF;


            END IF;

            --copy not null tab partition stats, only num rows and blocks are set, rest is left unchanged --pre istotu
            IF pv_no_rows IS NOT NULL AND pv_no_blocks IS NOT NULL THEN

                dbms_stats.copy_table_stats(OWNNAME=>c_t.table_owner, TABNAME=> c_t.table_name , SRCPARTNAME=>pv_src_part,
                DSTPARTNAME=>c_t.partition_name,SCALE_FACTOR=>c_t.scale_factor, force=>true);

                --backup global stats and backup dest partition
                IF p_backup_global THEN
                    dbms_stats.export_table_stats(ownname=>c_t.table_owner, tabname=>c_t.table_name, statown=>'DWH_ADM',
                    stattab=>'BACKUP_TABLE_STATS', cascade=>true);
                END IF;

                --computni and setni global stats
                /*
                SELECT round(pv_no_partitions * pv_no_rows * c_t.scale_factor ), round(pv_no_partitions *  pv_no_blocks * c_t.scale_factor)
                INTO pv_global_rows, pv_global_blocks
                FROM dual;
                */
                --global stats: spocitam vsetky predosle rows a pridam pocet z poslednej particie vynasobeny scale factorom
                SELECT round(((c_t.partition_position - 1) * pv_no_rows) + (pv_no_rows * c_t.scale_factor) ),
                round(((c_t.partition_position - 1) * pv_no_blocks) + ( pv_no_blocks * c_t.scale_factor))
                INTO pv_global_rows, pv_global_blocks
                FROM dual;

                dbms_stats.set_table_stats(OWNNAME=>c_t.table_owner, TABNAME=>c_t.table_name, NUMROWS=>pv_global_rows,
                NUMBLKS=>pv_global_blocks, no_invalidate=>true, FORCE=>true);


                dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                    substr(c_t.table_owner || '.' || c_t.table_name||'.'||c_t.partition_name,1,100),
                                   'End');
            END IF;
            --ELSE ak su statistiky predoslej particie null alebo 0, tak sprav avg vsetkych not null/not zero particii
            --(ako pri scale_factor = 1) a setni ich alebo posli mail


            COMMIT;

        END LOOP;

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'Loop tables END',
                                   'End Stats Setting');
        --1. lokni table stats
        /*
        begin
        dbms_stats.lock_table_stats(OWNNAME=>'DWH_ODS_CDRTOOL', TABNAME=>'TEST_GPRS_X_bachatero');
        commit;
        end;
        */
        --select * from dba_views where view_name like '%COL%STAT%'


    /*
        UPDATE DWH_ADM.TBL_SET_STAT_TABS
        SET ACTIVE = 'Y'
        WHERE (TABLE_NAME, TABLE_OWNER) NOT IN (SELECT TABLE_NAME,TABLE_OWNER  FROM DWH_ADM.TBL_SET_STAT_TABS B
        WHERE EXISTS (SELECT 1 FROM DBA_TAB_SUBPARTITIONS A
        WHERE A.TABLE_NAME = B.TABLE_NAME AND A.TABLE_OWNER = B.TABLE_OWNER))
    */
    /*
        select * from dba_TAB_STATS_HISTORY

        select * from DBA_OPTSTAT_OPERATIONS
        order by start_time desc
    */

        --pri subparticiach skopirujem
   END p_set_object_stats_old;


    procedure p_set_object_stats(p_table_name varchar2 default null, p_table_owner varchar2 default null, p_backup_global boolean default null) IS

        pv_procname         CONSTANT VARCHAR2(30) := 'SET_OBJECT_STATS';
        pv_src_part dba_tab_partitions.partition_name%type;
        --pv_last_part        dba_tab_partitions.partition_name%type;
        --pv_no_partitions    dba_tab_partitions.partition_position%type;
        pv_no_rows          dba_tab_partitions.num_rows%type := NULL;
        pv_no_blocks        dba_tab_partitions.blocks%type := NULL;
        pv_global_rows      number;
        pv_global_blocks    number;
        pv_not_null_parts   number; --pocet particii s poctom riadkov vacsim ako avg vsetkych particii
        pv_random_val       number;

        pp_part_key dba_part_key_columns.column_name%type;
        pp_part_key_type dba_tab_columns.data_type%TYPE;



        v_vystup_file       clob default empty_clob();
        v_mail_subj         varchar2(50):='Set statistics problem @DWHREP';


   BEGIN
        --return;
        --TODO: 1. subpartitions --nothing to solve
        --      2. set individual tables/partitions called from within dwh_adm loading jobs
        --      3. while using real scale_factor other than 1 do round num_rows to integer
        --      4. backup global stats --done
        --scale factor nerobi automaticky round poctu riadkov, pocet nie je cele cislo !
        --global stats mesacny num rows a blocks zo suctu particiovych num_rows a blocks
        --alebo sucet poslednej particie a aktual global stats
        --!!! aj tabulky subpartitiovane !!! -- done
        --nastavene iba konkretne tabulky, ktore uz historicke stats maju

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'START Stats Setting',
                                   'Loop tables Start');
        /*
        FOR c_t IN (SELECT table_owner, table_name, scale_factor
                     FROM dwh_adm.TBL_SET_STAT_TABS
                     WHERE active = 'Y' ) LOOP
        */
        --loop najnovsich particii, kt. su zaroven bez statistik
        FOR c_t IN ( SELECT a.table_owner, a.table_name, a.scale_factor, a.subpart, a.partkey_stat, b.partition_name, b.partition_position
                     FROM dwh_adm.TBL_SET_STAT_TABS a, dba_tab_partitions b
                     WHERE a.table_owner = b.table_owner AND a.table_name = b.table_name
                     AND a.active = 'Y' AND (b.last_analyzed IS NULL OR b.num_rows IS NULL)
                     AND b.partition_position = (SELECT max(partition_position)
                                                 FROM dba_tab_partitions c
                                                 WHERE c.table_name = a.table_name
                                                 AND c.table_owner = a.table_owner
                                                 --pridane kvoli MAX_VALUE particiam, ktore maju vzdy najvyssiu partition_position
                                                 AND c.partition_name not like '%MAX%'
                                                 --pridane kvoli PART_3000* particiam, tie nas netrapia, za normalnych okolnosti tu uz nebudeme
                                                 AND c.partition_name not like '%PART_3000%'

                                                ))
        LOOP
            dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname
                                   ,'Start',
                                   substr(c_t.table_owner || '.' || c_t.table_name||'.'||c_t.partition_name,1,100));


            --getni meno poslednej particie s null stats
            --pouzitie dba_tab_partitions, pretoze selekt z dba_tab_statistics je pomalsi
            /*
            SELECT partition_name, partition_position
            INTO pv_last_part, pv_no_partitions
            FROM  dba_tab_partitions
            WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
            AND partition_position = (SELECT max(partition_position)
                                      FROM dba_tab_partitions
                                      WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner );
            */

            --ak je scale factor > 1, getni last but one partition name - predposlednu particiu, its num_rows & blocks
            --scale_factor= 1 or scale_factor > 1
            IF  c_t.scale_factor > 1 THEN
                SELECT partition_name, num_rows, blocks
                INTO pv_src_part, pv_no_rows, pv_no_blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                AND partition_position = c_t.partition_position - 1;
            ELSE --ak je scale 1, t.z. ze raz je v particii vacsi, inokedy mensi pocet riadkov ,
                -->vyber  nahodne jednu not null/not zero particiu ako zdrojovu a tu skopiruj do target
                /*
                SELECT partition_name, num_rows, blocks
                INTO pv_src_part, pv_no_rows, pv_no_blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                AND partition_position = (SELECT round(dbms_random.value(1, c_t.partition_position -1 )) from dual);
                */
                --najprv insertni do temp tabulky nenulove particie s poctom num_rows vacsim ako priemer (kvoli aktualnym particiam, resp.
                --particiam, ktore su vytvorene 3 mesiace dopredu ako je aktualny run_date a je v nich insertnutych len par riadkov)
                --a potom nahodne vyber jednu z nich  a jej stats skopiruj do aktualnej target.
                EXECUTE IMMEDIATE 'truncate table dwh_adm.tbl_set_stats';

                INSERT INTO dwh_adm.tbl_set_stats
                SELECT rownum, table_owner,table_name,partition_name, num_rows, blocks
                FROM  dba_tab_partitions
                WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                --AND num_rows IS NOT null and num_rows <> 0;
                AND num_rows >= (SELECT avg(num_rows)FROM  dba_tab_partitions
                                 WHERE table_name = c_t.table_name
                                 AND table_owner = c_t.table_owner);

                pv_not_null_parts:=SQL%rowcount;

                IF   pv_not_null_parts > 0 THEN
                    SELECT partition_name, no_rows, no_blocks
                    INTO  pv_src_part, pv_no_rows, pv_no_blocks
                    FROM  dwh_adm.tbl_set_stats
                    WHERE  id_row =(SELECT round(dbms_random.value(1, pv_not_null_parts ))  FROM dual);
                ELSE
                    --posli mail !!!, ze nema co nasetovat/skopirovat & zavolaj klasicke pocitanie stats

                    dwh_adm.pkg_adm_log.p_do_error(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname
                                   ,'Neexistuje nenulova source particia',
                                   substr(c_t.table_owner || '.' || c_t.table_name,1,100));

                END IF;


            END IF;

            --copy not null tab partition stats, only num rows and blocks are set, rest is left unchanged --pre istotu
            IF pv_no_rows IS NOT NULL AND pv_no_blocks IS NOT NULL THEN

                dbms_stats.copy_table_stats(OWNNAME=>c_t.table_owner, TABNAME=> c_t.table_name , SRCPARTNAME=>pv_src_part,
                DSTPARTNAME=>c_t.partition_name,SCALE_FACTOR=>c_t.scale_factor, force=>true);

                --getni partition key column, if range than set....
                --get_col_stats

                --ak subpart = Y, nakopiruj aj stats subparticii particie pv_src_part
                IF c_t.subpart = 'Y' THEN
                    /*
                    INSERT INTO dwh_adm.tbl_set_subparts
                    SELECT  subpartition_name, subpartition_position
                    FROM dba_tab_subpartitions
                    WHERE table_name = c_t.table_name AND table_owner = c_t.table_owner
                    AND partition_name = c_t.partition_name;
                    */

                    FOR c_subpart IN (SELECT  src.subpartition_name src_subpart, dst.subpartition_name dst_subpart
                                FROM dba_tab_subpartitions src, dba_tab_subpartitions dst
                                WHERE src.table_name = c_t.table_name  AND src.table_owner = c_t.table_owner
                                AND src.table_name = dst.table_name and src.table_owner = dst.table_owner
                                AND src.partition_name = pv_src_part and dst.partition_name = c_t.partition_name
                                AND src.subpartition_position = dst.subpartition_position)
                    LOOP

                        BEGIN

                            dbms_stats.copy_table_stats(OWNNAME=>c_t.table_owner, TABNAME=> c_t.table_name , SRCPARTNAME=>c_subpart.src_subpart,
                            DSTPARTNAME=>c_subpart.dst_subpart,SCALE_FACTOR=>c_t.scale_factor, force=>true);

                        EXCEPTION WHEN OTHERS THEN
                            v_vystup_file := v_vystup_file ||   c_t.table_owner || ' '|| c_t.table_name || chr(10) || chr(13);
                            p_send_mail(v_vystup_file,v_mail_subj);
                            --NULL;
                        END;

                    END LOOP;

                END IF;


                --backup global stats and backup dest partition
                IF p_backup_global THEN
                    dbms_stats.export_table_stats(ownname=>c_t.table_owner, tabname=>c_t.table_name, statown=>'DWH_ADM',
                    stattab=>'BACKUP_TABLE_STATS', cascade=>true);
                END IF;

                --computni and setni global stats
                /*
                SELECT round(pv_no_partitions * pv_no_rows * c_t.scale_factor ), round(pv_no_partitions *  pv_no_blocks * c_t.scale_factor)
                INTO pv_global_rows, pv_global_blocks
                FROM dual;
                */
                --global stats: spocitam vsetky predosle rows a pridam pocet z poslednej particie vynasobeny scale factorom
                SELECT round(((c_t.partition_position - 1) * pv_no_rows) + (pv_no_rows * c_t.scale_factor) ),
                round(((c_t.partition_position - 1) * pv_no_blocks) + ( pv_no_blocks * c_t.scale_factor))
                INTO pv_global_rows, pv_global_blocks
                FROM dual;

                dbms_stats.set_table_stats(OWNNAME=>c_t.table_owner, TABNAME=>c_t.table_name, NUMROWS=>pv_global_rows,
                NUMBLKS=>pv_global_blocks, no_invalidate=>true, FORCE=>true);


                IF c_t.partkey_stat = 'Y' THEN

                    --GLOBAL column STATS partition key HIGH_VALUE
                    dwh_adm.pkg_set_stats.p_get_partition_key_column(c_t.table_name ,c_t.table_owner , pp_part_key, pp_part_key_type);

                    --dwh_adm.pkg_set_stats.p_set_column_stats(c_t.table_name, c_t.table_owner, c_t.partition_name, pp_part_key, pp_part_key_type);

                    --partition
                    dwh_adm.pkg_set_stats.p_set_col_stats(c_t.table_name ,c_t.table_owner ,'PARTITION' ,c_t.partition_name,pv_src_part,pp_part_key, pp_part_key_type);

                    --global
                    dwh_adm.pkg_set_stats.p_set_col_stats(c_t.table_name ,c_t.table_owner ,'GLOBAL' ,c_t.partition_name,NULL,pp_part_key, pp_part_key_type);

                --!!!! nastav high_value in global_stats
                --getni partitition key column
                    --getni jeho type
                    --if date
                            --if month partition set last_day_of month --last_day(to_date(SYSDATE, 'dd-mm-yy')) from dual
                            --else set current day
                    --if number
                --c_t.table_owner
                --c_t.table_owner.table_name


                END IF;
                --!!!! nastav high_value in global_stats
                --getni partitition key column
                    --getni jeho type
                    --if date
                            --if month partition set last_day_of month --last_day(to_date(SYSDATE, 'dd-mm-yy')) from dual
                            --else set current day
                    --if number
                --c_t.table_owner
                --c_t.table_owner.table_name



                dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                    substr(c_t.table_owner || '.' || c_t.table_name||'.'||c_t.partition_name,1,100),
                                   'End');
            END IF;
            --ELSE ak su statistiky predoslej particie null alebo 0, tak sprav avg vsetkych not null/not zero particii
            --(ako pri scale_factor = 1) a setni ich alebo posli mail


            COMMIT;

        END LOOP;

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name,
                                   pkc_subprocess_name,
                                   pkc_package || '.' || pv_procname,
                                   'Loop tables End',
                                   'END Stats Setting');
        --1. lokni table stats
        /*
        begin
        dbms_stats.lock_table_stats(OWNNAME=>'DWH_ODS_CDRTOOL', TABNAME=>'TEST_GPRS_X_bachatero');
        commit;
        end;
        */
        --select * from dba_views where view_name like '%COL%STAT%'


    /*
        UPDATE DWH_ADM.TBL_SET_STAT_TABS
        SET ACTIVE = 'Y'
        WHERE (TABLE_NAME, TABLE_OWNER) NOT IN (SELECT TABLE_NAME,TABLE_OWNER  FROM DWH_ADM.TBL_SET_STAT_TABS B
        WHERE EXISTS (SELECT 1 FROM DBA_TAB_SUBPARTITIONS A
        WHERE A.TABLE_NAME = B.TABLE_NAME AND A.TABLE_OWNER = B.TABLE_OWNER))
    */
    /*
        select * from dba_TAB_STATS_HISTORY

        select * from DBA_OPTSTAT_OPERATIONS
        order by start_time desc
    */

        --pri subparticiach skopirujem
   END p_set_object_stats;


    PROCEDURE p_get_partition_key_column(pp_table_name in dba_tables.table_name%type,pp_owner in dba_tables.owner%type, pp_part_key OUT
            dba_part_key_columns.column_name%type, pp_part_key_type OUT dba_tab_columns.data_type%TYPE ) as

        pv_part_key dba_part_key_columns.column_name%type;
        pv_part_key_type dba_tab_columns.data_type%TYPE;

    BEGIN
        --looks up partition key column and its datatype

        SELECT column_name
        INTO pp_part_key --pv_part_key
        FROM dba_part_key_columns
        WHERE name = pp_table_name  AND owner=pp_owner;

        SELECT data_type
        INTO pp_part_key_type --pv_part_key_type
        FROM dba_tab_columns
        WHERE table_name = pp_table_name AND owner=pp_owner
        AND column_name = pp_part_key;

    END p_get_partition_key_column;


    PROCEDURE p_set_column_stats(pp_table_name in dba_tables.table_name%type,pp_owner in dba_tables.owner%type,
        pp_partition_name IN dba_tab_partitions.partition_name%type, pp_part_key IN dba_part_key_columns.column_name%type
        , pp_part_key_type IN dba_tab_columns.data_type%TYPE)
    AS
        pv_procname  CONSTANT VARCHAR2(30) := 'P_SET_COLUMN_STATS';

        srec dbms_stats.statrec;
        m_distcnt number;
        m_density number;
        m_nullcnt number;
        m_avgclen number;
        NOVALS dbms_stats.datearray;
        NOVALS1 dbms_stats.numarray;
        --
        pv_prev_low_raw raw(32);
        pv_prev_high_raw raw(32);
        --date
        pv_min_value_date date;
        pv_high_value_date date;
        --number
        pv_min_value_number number;
        pv_high_value_number number;
        pv_high_value_char varchar2(9); --kvoli konverzii pri number formate YYYYMM981

    --!!! DISCLAIMER xbachatero 20121210 !!!!
    --procedura podporuje zatial iba DATE a NUMBER partition key columns
    --procedura podporuje zatial iba MONTHLY a DAILY partitions of date and number datatypes
    --supportovany format particii PART_YYYYMM, PART_YYYYMMDD a YYYYY_Q.._D...
    --low value of part key column sa zatial nemeni
    --funguje iba vtedy ak nie je aktualne histogram v global column stats.

    BEGIN

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name, pkc_subprocess_name,pkc_package || '.' || pv_procname,
                                    'START','Set column stats '||substr(pp_owner || '.' || pp_table_name||'.'||pp_part_key,1,60));

        dbms_stats.get_column_stats(
        ownname => pp_owner,
        tabname => pp_table_name,
        colname => pp_part_key,
        distcnt => m_distcnt,
        density => m_density,
        nullcnt => m_nullcnt,
        srec => srec,
        avgclen => m_avgclen);

        --low value & high value of global column stats for partitioning key column
        SELECT low_value, high_value
        INTO pv_prev_low_raw, pv_prev_high_raw
        FROM dba_tab_columns
        WHERE table_name = pp_table_name AND owner=pp_owner
        AND column_name = pp_part_key;

        IF pv_prev_low_raw IS NULL OR pv_prev_high_raw IS NULL THEN

            --mail. notifikacia, ak global stats je null, t.j. ak global column stats nie su vypocitane
            --pripadne ich vypocitat.
            null;
            return;
        END IF;

        IF pp_part_key_type = 'DATE' THEN

                dbms_stats.convert_raw_value(pv_prev_low_raw, pv_min_value_date);
                dbms_stats.convert_raw_value(pv_prev_high_raw, pv_high_value_date);  --previous date high value

                --podla mena a dlzky mena particie zistim, ci je to mesacna alebo denna particia,
                --!!!TODO: spravit tuto kontrolu na zaklade hodnoty pv_min_value_date a pv_high_value_date a nie podla nazvu pp_partition_name
                --nastavim last_day_of_month resp. aktualny den do globalnej statistiky high_value pre partitioning key column
                IF pp_partition_name like 'PART_%' AND LENGTH(pp_partition_name) = 11 THEN --monthly
                    --DWH_TL_USAGE.TRN_VPB_USAGE_UNBILLED.PART_201110
                    --tu by sa hodil regexp
                    --LAST_DAY(ADD_MONTHS(to_date(substr(201209980,1,6),'yyyymm'),1))
                    NOVALS := DBMS_STATS.DATEARRAY(pv_min_value_date,LAST_DAY(pv_high_value_date)); --koniec aktualneho mesiaca

                    dbms_output.put_line('monthly');
                    dbms_output.put_line('pv_min_value_date:'|| pv_min_value_date);

                ELSIF  pp_partition_name like 'Y%Q%M%D%' OR (pp_partition_name like 'PART_%' AND LENGTH(pp_partition_name) = 13) THEN   --daily
                    --DWH_TL_USAGE.TRN_VPB_USAGE_UNBILLED_DAILY.Y2011_Q4_M10_D14     --DWH_TL_CUSTOMER.TRN_TRAFFIC_DATA.PART_20111213
                    --ELSIF  REGEXP_LIKE(pp_partition_name, '^Y[[:alnum:]]{}$');

                    NOVALS := DBMS_STATS.DATEARRAY(pv_min_value_date,trunc(sysdate));   --aktualny date poslednej pridanej particie

                    dbms_output.put_line('daily');
                    dbms_output.put_line('pv_min_value_date:'|| pv_min_value_date);

                END IF;
                dbms_stats.prepare_column_values(srec, novals);

        ELSIF  pp_part_key_type = 'NUMBER' THEN
                --mesacne particie, t.j. high value sa posunie o jeden mesiac
                --DWH_TL_USAGE.TRN_VPB_USAGE.ID_DATE_BILL --   201211980 -->  201212980
                dbms_stats.convert_raw_value(pv_prev_low_raw, pv_min_value_number);
                dbms_stats.convert_raw_value(pv_prev_high_raw, pv_high_value_number);  --previous number high value

                --sem dat ... IF regexp_like(prev_number_high_value, '[[:alpha:]]{9}')

                pv_high_value_char := to_char(pv_high_value_number); --convert number to char
                --to_number(TO_CHAR(ADD_MONTHS(to_date(substr(201301980,1,6),'YYYYMM'),1),'YYYYMM')  || '980')
                pv_high_value_number:=to_number(TO_CHAR(ADD_MONTHS(to_date(substr(pv_high_value_char,1,6),'YYYYMM'),1),'YYYYMM')  || '980');


                NOVALS1 := DBMS_STATS.NUMARRAY(pv_min_value_number,pv_high_value_number);

                dbms_stats.prepare_column_values(srec, novals1);

                --pri NUMBER particiach treba setnut partition key column aj na urovni particie, nielen global stats column,
                --a tym prepisat 201212981 na 201212980, pretoze copy_stats nastavi hranicnu hodnotu 201212981 (range partition < 201212981) ako high_value,
                --namiesto realnej hodnoty *980,
                --ktora sa nachadza v particii, napr. pri kopirovani copy_table_stats z 201211 do 201212 nastavi high value
                --pre id_date_bill na 201212981 a nie 201212980, ktoru by realne nastavil, ak by sa na particii pocitali statistiky
                --a nie kopirovali. potom pri selekte na realny id_date_bill je zle odhadnuta kardinalita,
                --pretoze dany id_date_bill ()
        END IF;

        dbms_stats.set_column_stats(
        ownname => pp_owner,
        tabname => pp_table_name,
        colname => pp_part_key,
        distcnt => m_distcnt,
        density => m_density,
        nullcnt => m_nullcnt,
        srec => srec,
        avgclen => m_avgclen,
        force => true);


        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name, pkc_subprocess_name,pkc_package || '.' || pv_procname,
                                    'Set column stats '||substr(pp_owner || '.' || pp_table_name||'.'||pp_part_key,1,60),
                                   'END');


        --  LAST_DAY(ADD_MONTHS(to_date(substr(201209980,1,6),'yyyymm'),1)) from dual

    END p_set_column_stats;


  PROCEDURE p_set_col_stats(pp_table_name in dba_tables.table_name%TYPE,pp_owner in dba_tables.owner%TYPE,pp_stat_type varchar2,
        pp_partition_name IN dba_tab_partitions.partition_name%TYPE,pp_src_partition_name IN dba_tab_partitions.partition_name%TYPE default NULL,
        pp_part_key IN dba_part_key_columns.column_name%TYPE, pp_part_key_type IN dba_tab_columns.data_type%TYPE)
    AS
        pv_procname  CONSTANT VARCHAR2(30) := 'P_SET_COL_STATS';

        srec dbms_stats.statrec;
        m_distcnt number;
        m_density number;
        m_nullcnt number;
        m_avgclen number;
        NOVALS dbms_stats.datearray;
        NOVALS1 dbms_stats.numarray;
        --
        pv_prev_low_raw raw(32);
        pv_prev_high_raw raw(32);
        --date
        pv_min_value_date date;
        pv_high_value_date date;
        --number
        pv_min_value_number number;
        pv_high_value_number number;
        pv_min_value_char varchar2(9); --kvoli konverzii pri number formate YYYYMM981
        pv_high_value_char varchar2(9); --kvoli konverzii pri number formate YYYYMM981


    --!!! DISCLAIMER xbachatero 20121210 !!!!
    --procedura podporuje zatial iba DATE a NUMBER partition key columns
    --procedura podporuje zatial iba MONTHLY a DAILY partitions of date and number datatypes
    --supportovany format particii PART_YYYYMM, PART_YYYYMMDD a YYYYY_Q.._D...
    --low value of part key column sa zatial nemeni
    --funguje iba vtedy ak nie je aktualne histogram v global column stats, ani v zdrojovej particii !!!

    --TODO: nastavovat GLOBAL min_value pri tabulkach, ktorym sa dropuju najstarsie particie, podla retention hodnoty z dwh_adm.dwh_table

    BEGIN

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name, pkc_subprocess_name,pkc_package || '.' || pv_procname,
                                    'START','Set column stats '||substr(pp_owner || '.' || pp_table_name||'.'||pp_part_key,1,60));

        IF  pp_stat_type = 'GLOBAL' THEN


                dbms_stats.get_column_stats(
                ownname => pp_owner,
                tabname => pp_table_name,
                colname => pp_part_key,
                distcnt => m_distcnt,
                density => m_density,
                nullcnt => m_nullcnt,
                srec => srec,
                avgclen => m_avgclen);

                SELECT low_value, high_value
                INTO pv_prev_low_raw, pv_prev_high_raw
                FROM dba_tab_columns
                WHERE table_name = pp_table_name AND owner = pp_owner
                AND column_name = pp_part_key;


       ELSE
                SELECT low_value, high_value
                INTO pv_prev_low_raw, pv_prev_high_raw
                FROM dba_part_col_statistics
                WHERE table_name = pp_table_name AND owner=pp_owner
                AND column_name = pp_part_key
                AND partition_name = pp_src_partition_name ;


                dbms_stats.get_column_stats(
                ownname => pp_owner,
                tabname => pp_table_name,
                colname => pp_part_key,
                partname => pp_src_partition_name,
                distcnt => m_distcnt,
                density => m_density,
                nullcnt => m_nullcnt,
                srec => srec,
                avgclen => m_avgclen);

        END IF;

        IF pv_prev_low_raw IS NULL OR pv_prev_high_raw IS NULL THEN

                    --mail. notifikacia, ak global stats je null, t.j. ak global column stats nie su vypocitane
                    --pripadne ich vypocitat.
            null;
            RETURN;
        END IF;


        IF pp_part_key_type = 'DATE' THEN


                --!!!TODO: spravit tuto kontrolu na zaklade hodnoty pv_min_value_date a pv_high_value_date

                IF pp_stat_type = 'GLOBAL' THEN
                    dbms_stats.convert_raw_value(pv_prev_low_raw, pv_min_value_date);
                END IF;
               -- dbms_stats.convert_raw_value(pv_prev_high_raw, pv_high_value_date);  --previous date high value



                --podla mena a dlzky mena particie zistim, ci je to mesacna alebo denna particia,
                --!!!TODO: spravit tuto kontrolu na zaklade hodnoty pv_min_value_date a pv_high_value_date a nie podla nazvu pp_partition_name
                --nastavim last_day_of_month resp. aktualny den do globalnej statistiky high_value pre partitioning key column
                IF pp_partition_name like 'PART_%' AND LENGTH(pp_partition_name) = 11 THEN --monthly

                    IF pp_stat_type = 'PARTITION' THEN --pri particii nastav aj min aj max value

                        pv_min_value_date:=trunc(sysdate,'MON'); --first day of current month

                    END IF;

                    --DWH_TL_USAGE.TRN_VPB_USAGE_UNBILLED.PART_201110
                    --tu by sa hodil regexp

                    NOVALS := DBMS_STATS.DATEARRAY(pv_min_value_date,LAST_DAY(trunc(sysdate))); --koniec aktualneho mesiaca


                ELSIF  pp_partition_name like 'Y%Q%M%D%' OR (pp_partition_name like 'PART_%' AND LENGTH(pp_partition_name) = 13) THEN   --daily
                    --DWH_TL_USAGE.TRN_VPB_USAGE_UNBILLED_DAILY.Y2011_Q4_M10_D14     --DWH_TL_CUSTOMER.TRN_TRAFFIC_DATA.PART_20111213
                    --ELSIF  REGEXP_LIKE(pp_partition_name, '^Y[[:alnum:]]{}$');

                    IF pp_stat_type = 'PARTITION' THEN --pri particii nastav aj min aj max value

                        pv_min_value_date:=trunc(sysdate); -- current day of current month

                    END IF;


                    NOVALS := DBMS_STATS.DATEARRAY(pv_min_value_date,trunc(sysdate));   --aktualny date poslednej pridanej particie


                    --dbms_output.put_line('pv_min_value_date:'|| pv_min_value_date);

                END IF;
                dbms_stats.prepare_column_values(srec, novals);

        ELSIF  pp_part_key_type = 'NUMBER' THEN --AND pp_stat_type IN ('GLOBAL','PARTITION') THEN
                --mesacne particie, t.j. high value sa posunie o jeden mesiac
                --DWH_TL_USAGE.TRN_VPB_USAGE.ID_DATE_BILL --   201211980 -->  201212980



                IF pp_stat_type = 'GLOBAL' THEN

                    dbms_stats.convert_raw_value(pv_prev_low_raw, pv_min_value_number);

                END IF;
                --dbms_stats.convert_raw_value(pv_prev_high_raw, pv_high_value_number);  --previous number high value

                --sem dat ... IF regexp_like(prev_number_high_value, '[[:alpha:]]{9}')

                IF pp_stat_type = 'PARTITION' THEN --pri particii nastav aj min aj max value


                     --pv_min_value_char := to_char(pv_min_value_number); --convert number to char
                     --pv_min_value_number:=to_number(TO_CHAR(ADD_MONTHS(to_date(substr(pv_min_value_char,1,6),'YYYYMM'),1),'YYYYMM')  || '980');
                     pv_min_value_number:=to_number(to_char(sysdate,'YYYYMM')|| '980');


                END IF;

                --pv_high_value_char := to_char(pv_high_value_number); --convert number to char
                --to_number(TO_CHAR(ADD_MONTHS(to_date(substr(201301980,1,6),'YYYYMM'),1),'YYYYMM')  || '980')
                --pv_high_value_number:=to_number(TO_CHAR(ADD_MONTHS(to_date(substr(pv_high_value_char,1,6),'YYYYMM'),1),'YYYYMM')  || '980');
                pv_high_value_number:=to_number(to_char(sysdate,'YYYYMM')|| '980');

                NOVALS1 := DBMS_STATS.NUMARRAY(pv_min_value_number,pv_high_value_number);

                dbms_stats.prepare_column_values(srec, novals1);


                --pri NUMBER particiach treba setnut partition key column aj na urovni particie, nielen global stats column,
                --a tym prepisat 201212981 na 201212980, pretoze copy_stats nastavi hranicnu hodnotu 201212981 (range partition < 201212981) ako high_value,
                --namiesto realnej hodnoty *980,
                --ktora sa nachadza v particii, napr. pri kopirovani copy_table_stats z 201211 do 201212 nastavi high value
                --pre id_date_bill na 201212981 a nie 201212980, ktoru by realne nastavil, ak by sa na particii pocitali statistiky
                --a nie kopirovali. potom pri selekte na realny id_date_bill je zle odhadnuta kardinalita,
                --pretoze dany id_date_bill je out of range ()
        END IF;



        IF  pp_stat_type = 'GLOBAL' THEN

                dbms_stats.set_column_stats(
                ownname => pp_owner,
                tabname => pp_table_name,
                colname => pp_part_key,
                distcnt => m_distcnt,
                density => m_density,
                nullcnt => m_nullcnt,
                srec => srec,
                avgclen => m_avgclen,
                force => true);

        ELSE
                dbms_stats.set_column_stats(
                ownname => pp_owner,
                tabname => pp_table_name,
                colname => pp_part_key,
                partname =>pp_partition_name,
                distcnt => m_distcnt,
                density => m_density,
                nullcnt => m_nullcnt,
                srec => srec,
                avgclen => m_avgclen,
                force => true);

        END IF;

        dwh_adm.pkg_adm_log.p_do_log(pkc_process_name, pkc_subprocess_name,pkc_package || '.' || pv_procname,
                                    'Set column stats '||substr(pp_owner || '.' || pp_table_name||'.'||pp_part_key,1,60),
                                   'END');

        EXCEPTION when OTHERS then

             dwh_adm.pkg_adm_log.p_do_log(pkc_process_name, pkc_subprocess_name,pkc_package || '.' || pv_procname,
                                    sqlerrm,'ERROR');

    END p_set_col_stats;




    procedure p_send_mail (p_vystup_file IN CLOB, p_mail_subj IN varchar2) as

        v_mail_addressee    varchar2(25):='x_bachatero@bachatero.sk'; -- 'x_bachatero@bachatero.sk','dwhdba@bachatero.sk'
        v_msg_id            number;
        v_att               UM_client.t_attachment := UM_client.t_attachment(null, null, null);
        v_zoznam_att        UM_client.t_attachment_list := UM_client.t_attachment_list();
        v_vystup_file       clob default empty_clob();

    BEGIN
        v_vystup_file := p_vystup_file;
        um_client.k_mail_klient.send_mail('dwh',
        null,
        v_mail_addressee,
        null,
        null,
        p_mail_subj,
        um_client.k_mail_klient.c_priority_medium,
        false,
        v_vystup_file,
        v_zoznam_att,
        v_msg_id);

    END p_send_mail;

END pkg_set_stats;
/


-- End of DDL Script for Package Body DWH_ADM.PKG_SET_STATS

