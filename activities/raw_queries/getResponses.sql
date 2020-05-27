select
	rfov.respuesta_ptr_id id_resp,
    marca.id id_marca,
	marca.nombre,
	CAST(Case
            When rfov."esVerdadero"=true Then 'Verdadero'
            ELse 'Falso' END
        AS VARCHAR) as respuesta,
	CASE When pfov."esVerdadero"=rfov."esVerdadero" Then 5 else 0 end calificacion,
	resp.intento
from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	inner join activities_respuestavof rfov on actividad.id = rfov."preguntaVoF_id"
	inner join activities_preguntafov pfov on rfov."preguntaVoF_id" = pfov."actividad_ptr_id"
	inner join activities_respuesta resp on resp.id = rfov.respuesta_ptr_id
	where marca.contenido_id = %s and resp.estudiante_id = %s and marca.id = %s
union all
select
    rpa.respuesta_ptr_id id_resp,
    marca.id id_marca,
	marca.nombre,
	rpa.respuesta as respuesta,
	rca.calificacion calificacion,
	resp.intento
from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	inner join activities_respuestaabiertaestudiante rpa on actividad.id = rpa."preguntaAbierta_id"
	inner join activities_respuesta resp on resp.id = rpa.respuesta_ptr_id
	left join activities_calificacion rca on rca.actividad_id=rpa."preguntaAbierta_id"
	where marca.contenido_id = %s and resp.estudiante_id = %s and marca.id = %s
union all
select
	rme.respuestmultiple_id id_resp,
    marca.id id_marca,
	marca.nombre,
	om.opcion as respuesta,
	((case When om."esCorrecta"=true then 5 else 0 end)::NUMERIC /(select (count(*))::NUMERIC from activities_opcionmultiple where "preguntaSeleccionMultiple_id"=om."preguntaSeleccionMultiple_id")) calificacion,
	resp.intento
	from
	activities_actividad actividad
	inner join activities_marca marca on marca.id = actividad.marca_id
	inner join activities_preguntaopcionmultiple pom on pom.actividad_ptr_id = actividad.id
	inner join activities_opcionmultiple om on om."preguntaSeleccionMultiple_id" = pom.actividad_ptr_id
	inner join activities_respuestmultipleestudiante rme on rme.respuestmultiple_id  = om.id
	inner join activities_respuesta resp on resp.id = rme.respuesta_ptr_id
	where marca.contenido_id = %s and resp.estudiante_id = %s and marca.id = %s
order by 6 desc