from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Room, Reservation
from .forms import RoomForm, ReservationForm
from datetime import date


class Home(View):
    def get(self, request):
        template_name = 'home.html'
        return render(request, template_name)


class NewRoom(View):
    def get(self, request):
        template_name = 'new_room.html'
        form = RoomForm()
        return render(request, template_name, {
            'form': form,
        })

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')


class ModifyRoom(View):
    def get(self, request, id):
        template_name = 'new_room.html'
        room = Room.objects.get(pk=id)
        form = RoomForm(initial={
            'name': room.name,
            'capacity': room.capacity,
            'is_projector_available': room.is_projector_available,
        })

        return render(request, template_name, {
            'form': form,
            'room': room,
        })

    def post(self, request, id):
        instance = get_object_or_404(Room, pk=id)
        form = RoomForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('home')


class DeleteRoom(View):
    def get(self, request, id):
        Room.objects.get(pk=id).delete()
        return redirect('home')


class ShowRoom(View):
    def get(self, request, id):
        template_name = 'show_room.html'
        today = date.today()
        room = Room.objects.get(pk=id)
        reservations = Reservation.objects.filter(room=room).filter(date__gte=today).order_by('date')

        return render(request, template_name, {
            'room': room,
            'reservations': reservations
        })


class AllRooms(View):
    def get(self, request):
        template_name = 'all_rooms.html'
        rooms = Room.objects.all()
        today = date.today()
        reservations = Reservation.objects.filter(date=today)
        reserved_rooms_id = []
        for reservation in reservations:
            if reservation.room in rooms:
                reserved_rooms_id.append(reservation.room_id)

        return render(request, template_name, {
            'rooms': rooms,
            'reserved_rooms_id': reserved_rooms_id,
        })


class ReservationView(View):
    def get(self, request, room_id):
        template_name = 'reservation.html'
        room = Room.objects.get(pk=room_id)
        form = ReservationForm()
        today = date.today()
        reservations = Reservation.objects.filter(room=room).filter(date__gte=today).order_by('date')

        return render(request, template_name, {
            'form': form,
            'room': room,
            'reservations': reservations,
        })

    def post(self, request, room_id):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            today = date.today()
            if reservation.date >= today:
                reservation.room_id = room_id
                try:
                    reservation.save()
                except IntegrityError:
                    error_message = "Sala już jest zarezerwowana tego dnia, wybierz inną datę"
                    return self.render_reservation(request, room_id, error_message)
            else:
                error_message = "Data którą wprowadziłeś jest z przeszłości, wprowadź poprawną datę"
                return self.render_reservation(request, room_id, error_message)

        return redirect('home')

    @staticmethod
    def render_reservation(request, room_id, error_message):
        template_name = 'reservation.html'
        form = ReservationForm()
        today = date.today()
        room = Room.objects.get(pk=room_id)
        reservations = Reservation.objects.filter(room=room).filter(date__gte=today).order_by('date')
        return render(request, template_name, {
            'form': form,
            'room': room,
            'reservations': reservations,
            'error_message': error_message,
        })


class SearchRoom(View):
    def get(self, request):
        template_name = 'searched_rooms.html'
        rooms = Room.objects.all()
        if request.GET.get('name'):
            name = request.GET.get('name')
            rooms = rooms.filter(name__icontains=name)
        if request.GET.get('capacity'):
            capacity = request.GET.get('capacity')
            rooms = rooms.filter(capacity__gte=capacity)
        if request.GET.get('reservation__date'):
            reservation__date = request.GET.get('reservation__date')
            rooms = rooms.exclude(reservation__date=reservation__date)
        if request.GET.get('is_projector_available'):
            is_projector_available = request.GET.get('is_projector_available')
            if is_projector_available:
                rooms = rooms.filter(is_projector_available=True)
        message = None
        if not rooms.exists():
            message = "Brak wolnych sal dla podanych kryteriów wyszukiwania"
        return render(request, template_name, {
            'rooms': rooms,
            'message': message,
        })
