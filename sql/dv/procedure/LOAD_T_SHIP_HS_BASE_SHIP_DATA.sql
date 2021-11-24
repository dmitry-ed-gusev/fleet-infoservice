create procedure dv.load_t_ship_hs_base_ship_data ()
begin
	
	insert into dv.t_ship_hs (ship_id, valid_from, flag, main_name, secondary_name, home_port, call_sign, row_hash, load_dttm)
	select h.ship_id, str_to_date(stg.datetime, '%d-%b-%Y %T') as valid_from, stg.flag, stg.main_name, 
		stg.secondary_name, stg.home_port, stg.call_sign, md5(concat_ws('#', stg.flag, stg.main_name, stg.secondary_name, stg.home_port, stg.call_sign)) as row_hash, sysdate()
	from stage.base_ship_data stg
		join dv.t_ship_h h
			on (stg.imo_number = h.imo_num or (stg.imo_number is null and h.imo_num is null))
				and (stg.proprietary_number = h.reg_num or (stg.proprietary_number is null and h.reg_num is null))
                and stg.source_system = h.src_nm
		left join dv.t_ship_hs tgt
			on h.ship_id = tgt.ship_id
				and tgt.valid_to is null
				and tgt.row_hash = md5(concat_ws('#', stg.flag, stg.main_name, stg.secondary_name, stg.home_port, stg.call_sign))
	where tgt.ship_id is null;
        
	update dv.t_ship_hs as tgt,
		(
			select ship_id, valid_from, valid_to_new
			from (
				select ship_id, valid_from, valid_to, max(valid_from) over (partition by ship_id order by valid_from asc rows between 1 following and 1 following) as valid_to_new
				from dv.t_ship_hs
			) x
			where valid_to_new is not null and (valid_to <> valid_to_new or valid_to is null)
		) as src
	set tgt.valid_to = src.valid_to_new
    where tgt.ship_id = src.ship_id
		and tgt.valid_from = src.valid_from;
end;
