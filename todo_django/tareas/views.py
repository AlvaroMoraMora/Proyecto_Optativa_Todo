from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Tarea, Prioridad


def lista_tareas(request):
    filtro = request.GET.get('filtro', 'todas')
    busqueda = request.GET.get('busqueda', '')
    
    tareas = Tarea.objects.all()
    
    if busqueda:
        tareas = tareas.filter(
            Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )
    
    if filtro == 'pendientes':
        tareas = tareas.filter(completada=False)
    elif filtro == 'completadas':
        tareas = tareas.filter(completada=True)
    
    total = Tarea.objects.count()
    pendientes = Tarea.objects.filter(completada=False).count()
    completadas = Tarea.objects.filter(completada=True).count()
    urgentes = Tarea.objects.filter(prioridad=Prioridad.ALTA, completada=False).count()
    
    progreso = (completadas / total * 100) if total > 0 else 0
    
    context = {
        'tareas': tareas,
        'filtro': filtro,
        'busqueda': busqueda,
        'stats': {
            'total': total,
            'pendientes': pendientes,
            'completadas': completadas,
            'urgentes': urgentes,
            'progreso': progreso,
        }
    }
    return render(request, 'tareas/lista.html', context)


def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        fecha_limite = request.POST.get('fecha_limite')
        fecha_limite = fecha_limite if fecha_limite else None
        prioridad = int(request.POST.get('prioridad', 2))
        etiquetas = request.POST.get('etiquetas', '')
        
        Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_limite=fecha_limite,
            prioridad=prioridad,
            etiquetas=etiquetas
        )
        messages.success(request, '¡Tarea creada correctamente!')
        return redirect('lista_tareas')
    
    return render(request, 'tareas/crear.html', {'prioridades': Prioridad.choices})


def editar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion', '')
        tarea.fecha_limite = request.POST.get('fecha_limite') or None
        tarea.prioridad = int(request.POST.get('prioridad', 2))
        tarea.etiquetas = request.POST.get('etiquetas', '')
        tarea.save()
        
        messages.success(request, '¡Tarea actualizada correctamente!')
        return redirect('lista_tareas')
    
    return render(request, 'tareas/editar.html', {
        'tarea': tarea,
        'prioridades': Prioridad.choices
    })


def eliminar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, '¡Tarea eliminada correctamente!')
    return redirect('lista_tareas')


def toggle_completada(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completada = not tarea.completada
    tarea.save()
    estado = 'completada' if tarea.completada else 'pendiente'
    messages.success(request, f'Tarea marcada como {estado}')
    return redirect('lista_tareas')
