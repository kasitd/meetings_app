from django.forms import ModelForm, DateInput, TimeInput
from .models import Meeting
from datetime import datetime, timedelta, date, time


def check_vacancy(day, start, end, room):
    return Meeting.objects.filter(room=room).filter(date=day).filter(end_time__gt=start, start_time__lt=end).exists()


def get_time_slots(day, room):
    times = Meeting.objects.filter(room=room).filter(date=day).order_by('start_time').\
        values_list('start_time', 'end_time')
    meetings = list(times)
    flat_times = [val.strftime("%H:%M") for times in meetings for val in times]
    flat_times.insert(0, '06:00')  # rozpoczęcie pracy biura
    flat_times.append('18:00')  # zakończenie pracy biura
    empty = []
    for i, t in enumerate(flat_times):
        if i + 1 < len(flat_times):
            if i % 2 == 0:
                if flat_times[i] != flat_times[i + 1]:
                    empty.append(flat_times[i] + "-" + flat_times[i + 1])
    return ", ".join(empty)



def get_year_later():
    return datetime.now().date() + timedelta(days=365)


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'date': DateInput(attrs={"type": "date"}),
            'start': TimeInput(attrs={"type": "time"}),
            'end': TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("date")
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        rroom = cleaned_data.get('room')
        if start_date < date.today():
            msg = "Nie można wybrać daty wstecznej"
            self.add_error('date', msg)
        if start > end:
            msg1 = "Zakończenie nie może być przed rozpoczęciem"
            self.add_error('end_time', msg1)
        if check_vacancy(start_date, start, end, rroom):
            msg2 = 'w wybranych godzinach sala jest zajęta'
            self.add_error('room', msg2)
            if len(get_time_slots(start_date, rroom)) == 0:
                msg3 = f"w dniu {start_date} w sali {rroom} nie ma wolnych terminów".format(start_date=start_date,
                                                                                            rroom=rroom)
                self.add_error('room', msg3)
            else:
                times = get_time_slots(start_date, rroom)
                msg4 = f"dostępne godziny w wybranej sali: {times}".format(times=times)
                self.add_error('room', msg4)



