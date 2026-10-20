from django.shortcuts import render
from storage import load_polls, load_votes
from voting_logic import get_poll_results

def poll_list(request):
    polls_dict = load_polls("data/polls.json")
    polls_list = []
    for poll_id, poll_data in polls_dict.items():
        poll_data['id'] = int(poll_id) 
        polls_list.append(poll_data)
    return render(request, "votes/poll_list.html", {"polls": polls_list})

def poll_detail(request, poll_id):
    polls_dict = load_polls("data/polls.json")
    current_poll = polls_dict.get(str(poll_id))
    
    # Если голосование не найдено, мы НЕ вызываем get_poll_results, 
    # а сразу идем в шаблон, передавая poll=None
    if current_poll is None:
        return render(
            request, 
            "votes/poll_detail.html", 
            {"poll": None}, 
            status=404
        )

    # Если голосование найдено, считаем результаты
    votes = load_votes("data/votes.json")
    results_dict = get_poll_results(polls_dict, votes, int(poll_id))
    
    choices_with_results = []
    if results_dict:
        for choice_name, count in results_dict.items():
            choices_with_results.append({"name": choice_name, "count": count})
    else:
        for choice_id, choice_name in current_poll["choices"].items():
            choices_with_results.append({"name": choice_name, "count": 0})

    # Передаем данные в шаблон, статус 200
    return render(
        request,
        "votes/poll_detail.html",
        {
            "poll": current_poll,
            "choices_data": choices_with_results,
        },
        status=200
    )
