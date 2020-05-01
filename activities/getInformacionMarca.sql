select
	distinct actividad.id,
	actividad.marca_id,
	actividad."tipoActividad",
	marca.punto,
	marca.nombre,
	marca.contenido_id,
	actividad."numeroDeIntentos"- count(rfov."preguntaVoF_id" ) as numIntentos
from
	activities_actividad actividad
inner join activities_marca marca on
	marca.id = actividad.marca_id
inner join activities_preguntafov pfov on pfov.actividad_ptr_id = actividad.id
left join activities_respuestavof rfov on actividad.id = rfov."preguntaVoF_id"
where
	marca.contenido_id = %s
group by
	actividad.id,
	marca.punto,
	actividad.marca_id,
	actividad."tipoActividad",
	marca.punto,
	marca.nombre,
	marca.contenido_id,
	actividad."numeroDeIntentos"
union
select
	distinct actividad.id,
	actividad.marca_id,
	actividad."tipoActividad",
	marca.punto,
	marca.nombre,
	marca.contenido_id,
	actividad."numeroDeIntentos"- count(rpa."preguntaAbierta_id" ) as numIntentos
from
	activities_actividad actividad
inner join activities_marca marca on
	marca.id = actividad.marca_id
inner join activities_preguntaabierta pa on pa.actividad_ptr_id = actividad.id
left join activities_respuestaabiertaestudiante rpa on actividad.id = rpa."preguntaAbierta_id"
where
	marca.contenido_id = %s
group by
	actividad.id,
	marca.punto,
	actividad.marca_id,
	actividad."tipoActividad",
	marca.punto,
	marca.nombre,
	marca.contenido_id,
	actividad."numeroDeIntentos"