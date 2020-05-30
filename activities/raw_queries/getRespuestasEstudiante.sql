select
    marca.id,
	CAST(Case
            When rfov."esVerdadero"=true Then 'Verdadero'
            ELse 'Falso' END
        AS VARCHAR) as respuesta
from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	left join activities_respuestavof rfov on actividad.id = rfov."preguntaVoF_id"
where rfov.respuesta_ptr_id =
	(select
		resp.id
	from
		activities_actividad actividad
		inner join activities_marca marca on marca.id = actividad.marca_id
		inner join activities_respuestavof rfov on actividad.id = rfov."preguntaVoF_id"
		inner join activities_respuesta resp on resp.id = rfov.respuesta_ptr_id	
	where
		marca.contenido_id = %s and resp.estudiante_id = %s and marca.id = %s
	order by resp.fecha_creacion desc
	limit 1)
union
select
    marca.id,
	CAST (rpa.respuesta AS VARCHAR ) as respuesta
from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	left join activities_respuestaabiertaestudiante rpa on actividad.id = rpa."preguntaAbierta_id"
where rpa.respuesta_ptr_id =
	(select
		resp.id
	from
		activities_actividad actividad
		inner join activities_marca marca on marca.id = actividad.marca_id
		inner join activities_respuestaabiertaestudiante rpa on actividad.id = rpa."preguntaAbierta_id"
		inner join activities_respuesta resp on resp.id = rpa.respuesta_ptr_id		
	where
		marca.contenido_id = %s and resp.estudiante_id = %s and marca.id = %s
	order by resp.fecha_creacion desc
	limit 1)
union
select
    marca.id,
	CAST (om.opcion AS VARCHAR ) as respuesta
from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	inner join activities_preguntaopcionmultiple pom on pom.actividad_ptr_id = actividad.id
	inner join activities_opcionmultiple om on om."preguntaSeleccionMultiple_id" = pom.actividad_ptr_id
	inner join activities_respuestmultipleestudiante rme on rme.respuestmultiple_id  = om.id
	inner join activities_respuesta resp on resp.id = rme.respuesta_ptr_id
where marca.id=%s and resp.intento =
	(select
		resp.intento
	from
			activities_actividad actividad
			inner join activities_marca marca on marca.id = actividad.marca_id
			inner join activities_preguntaopcionmultiple pom on pom.actividad_ptr_id = actividad.id
			inner join activities_opcionmultiple om on om."preguntaSeleccionMultiple_id" = pom.actividad_ptr_id
			inner join activities_respuestmultipleestudiante rme on rme.respuestmultiple_id  = om.id
			inner join activities_respuesta resp on resp.id = rme.respuesta_ptr_id
	where
		marca.contenido_id = %s and resp.estudiante_id = %s and marca.id=%s
	order by resp.intento desc
	limit 1)