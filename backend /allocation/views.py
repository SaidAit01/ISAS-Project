from django.http import JsonResponse
from .models import SupervisorProfile, StudentProposal
from .services import calculate_academic_fit
from .algorithms import generate_hybrid_preferences, spa_allocation

def run_allocation_algorithm(request):
    #  Fetch Data from the db
    supervisors = list(SupervisorProfile.objects.all())
    students = list(StudentProposal.objects.all())
    
    if not supervisors or not students:
        return JsonResponse({"error": "No data found. Add supervisors and students first."}, status=400)

    
    # Extract just the text for SBERT
    student_texts = [s.topic_description for s in students]
    supervisor_texts = [s.research_interests for s in supervisors]
    
    # Extract names and choices for the Algorithms
    supervisor_names = [s.name for s in supervisors]
    student_choices = [s.manual_preferences for s in students]
    
    # Create a capacity dictionary { 'Dr. Smith': 5, ... }
    capacities = {s.name: s.capacity for s in supervisors}

   
    # This calls the SBERT function
    score_matrix = calculate_academic_fit(student_texts, supervisor_texts)

   
    # This calls the Hybrid List function
    preference_data = generate_hybrid_preferences(
        student_choices, 
        supervisor_names, 
        score_matrix, 
        n_limit=10
    )

    #We must convert the LISTS into DICTIONARIES before sending to SPA.
    # The 'enumerate' function gives us the ID (0, 1, 2...) for each person.
    
    student_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['students'])}
    supervisor_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['supervisors'])}

    # 5. EXECUTE ALLOCATION (Block 3)
    final_matches = spa_allocation(
        student_prefs_dict,      # <--- Pass the new Dictionary
        supervisor_prefs_dict,   # <--- Pass the new Dictionary
        capacities,
        supervisor_names
    )


    return JsonResponse({
        "status": "success",
        "matches": final_matches,
        "debug_preferences": preference_data # Helpful for seeing what the AI thought
    })