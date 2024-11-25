from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import Result, Member, Statistics, Course, MetrixUserMapping
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime


class MyCompetitionsView(View):
    template_name = 'my_competitions.html'

    def get(self, request, *args, **kwargs):
        member_id = request.user.id
        member = Member.objects.get(id=member_id)

        api_url = "https://discgolfmetrix.com/api.php"
        params = {
            'content': 'my_competitions',
            'code': member.metrix_code,
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        competition_ids = data.get('my_competitions', [])

        competitions_info = []

        for competition_id in competition_ids:
            # Dla każdego zawodu, pobierz dodatkowe informacje
            competition_params = {
                'content': 'result',
                'id': competition_id,
                'code': member.metrix_code,
            }

            competition_response = requests.get(api_url, params=competition_params)
            competition_data = competition_response.json().get('Competition', {})

            # Sprawdź, czy kurs istnieje w bazie danych, jeśli nie, dodaj go
            course_id = competition_data.get('CourseID')
            course_name = competition_data.get('CourseName')
            course, created = Course.objects.get_or_create(
                course_id=course_id,
                defaults={'name': course_name}  # Możesz dodać więcej pól, jeśli są dostępne w API
            )

            competitions_info.append({
                'competition_id': competition_data.get('ID'),
                'name': competition_data.get('Name'),
                'date': competition_data.get('Date'),
                'time': competition_data.get('Time'),
                'course_name': course.name,
                'course_id': course.course_id,
            })

        context = {'competitions_info': competitions_info}
        return render(request, self.template_name, context)


class CompetitionResultsView(View):
    template_name = 'competition_results.html'

    def get(self, request, competition_id, *args, **kwargs):
        member_id = request.user.id
        member = Member.objects.get(id=member_id)

        api_url = "https://discgolfmetrix.com/api.php"
        params = {
            'content': 'result',
            'id': competition_id,
            'code': member.metrix_code,
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        competition_data = data.get('Competition', {})
        results_data = competition_data.get('Results', [])

        course_id_from_api = competition_data.get('CourseID')
        course, _ = Course.objects.get_or_create(course_id=course_id_from_api)

        competition_id_from_api = str(competition_data.get('ID'))



        results = []

        for result_data in results_data:
            order_number = result_data.get('OrderNumber')
            if order_number is not None:
                track_info = next(
                    (track for track in competition_data.get('Tracks', []) if track.get('Number') == str(order_number)),
                    {})
                hole_number = track_info.get('Number')

                hole_result = result_data.get('Result')

                metrix_user_id = result_data.get('UserID')
                your_app_user_mapping, created = MetrixUserMapping.objects.get_or_create(metrix_user_id=metrix_user_id)
                your_app_user = your_app_user_mapping.your_app_user

                if hole_result is not None:
                    result, created = Result.objects.get_or_create(
                        member=your_app_user,
                        course=course,
                        competition_id=competition_id_from_api,
                        date=datetime.strptime(competition_data.get('Date'), "%Y-%m-%d"),
                        hole_number=hole_number,
                        hole_result=hole_result,
                        hole_diff=result_data.get('Diff'),
                    )

                    results.append({
                        'user_id': result_data.get('UserID'),
                        'name': result_data.get('Name'),
                        'class_name': result_data.get('ClassName'),
                        'country_code': result_data.get('CountryCode'),
                        'group': result_data.get('Group'),
                        'player_results': result_data.get('PlayerResults', []),
                        'penalty': result_data.get('Penalty'),
                        'sum': result_data.get('Sum'),
                        'diff': result_data.get('Diff'),
                        'dnf': result_data.get('DNF'),
                        'previous_rounds_sum': result_data.get('PreviousRoundsSum'),
                        'previous_rounds_diff': result_data.get('PreviousRoundsDiff'),
                        'order_number': result_data.get('OrderNumber'),
                    })

        context = {'competition_data': competition_data, 'results': results}
        return render(request, self.template_name, context)

@login_required
def my_statistics(request):
    user = request.user
    member = Member.objects.get(user=user)
    results = Result.objects.filter(member=member).values('competition_id').distinct()

    statistics, created = Statistics.objects.get_or_create(member=member)
    statistics.total_competitions = results.count()
    statistics.total_throws = sum(result.hole_result for result in Result.objects.filter(member=member))
    statistics.total_difference_to_par = sum(result.hole_diff for result in Result.objects.filter(member=member))
    statistics.save()

    context = {
        'statistics': statistics,
    }

    return render(request, 'my_statistics.html', context)
