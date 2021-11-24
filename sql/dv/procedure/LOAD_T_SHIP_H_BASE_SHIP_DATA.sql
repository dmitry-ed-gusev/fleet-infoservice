create procedure dv.load_t_ship_h_base_ship_data ()
begin
	declare max_id integer;

	select coalesce(max(ship_id),0)
    into max_id
    from dv.t_ship_h;

	insert into dv.t_ship_h (ship_id, imo_num, reg_num, src_nm, load_dttm)
		select max_id + row_number() over (), imo_number, proprietary_number, source_system, sysdate()
		from stage.base_ship_data stg
			left join dv.t_ship_h tgt
				on (stg.imo_number = tgt.imo_num or (stg.imo_number is null and tgt.imo_num is null))
					and (stg.proprietary_number = tgt.reg_num or (stg.proprietary_number is null and tgt.reg_num is null))
                    and stg.source_system = tgt.src_nm 
		where tgt.ship_id is null
		group by imo_number, proprietary_number, source_system;
end;
